"""Isolated domain/transaction tests. These are partial evidence, not full control acceptance."""
import importlib.util
import json
import sqlite3
import tempfile
import unittest
import uuid
from pathlib import Path

WORK = Path(__file__).resolve().parent
MODULE = WORK.parent / "app/experience.py"
spec = importlib.util.spec_from_file_location("trail_experience", MODULE)
experience = importlib.util.module_from_spec(spec)
spec.loader.exec_module(experience)


class ExperienceTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix="experience-test-", dir=WORK)
        self.path = Path(self.folder.name) / "fixture.sqlite"
        self.db = sqlite3.connect(self.path, isolation_level=None)
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript("""
          CREATE TABLE campaign(singleton INTEGER PRIMARY KEY,campaign_id TEXT UNIQUE,revision INTEGER,next_day_number INTEGER);
          CREATE TABLE hike_day(day_number INTEGER PRIMARY KEY,day_id TEXT UNIQUE,status TEXT);
          CREATE TABLE completion(operation_id TEXT PRIMARY KEY,day_id TEXT UNIQUE);
          INSERT INTO campaign VALUES(1,'test-campaign',0,1);
          INSERT INTO hike_day VALUES(1,'day-001','active');
        """)
        self.db.execute("BEGIN IMMEDIATE")
        experience.ensure_schema(self.db, 4)
        self.assertTrue(self.db.in_transaction)
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.folder.cleanup()

    def state(self):
        row = self.db.execute("SELECT campaign_id,revision FROM campaign").fetchone()
        day = self.db.execute("SELECT day_id FROM hike_day WHERE status='active'").fetchone()
        return {"campaign_id": row[0], "revision": row[1], "current_day_id": day[0] if day else None, "total_days": 4}

    def view(self, day="day-001"):
        return experience.get_experience(self.db, self.state(), day)

    def body(self, **fields):
        view = self.view()
        return {"day_id": "day-001", "operation_id": str(uuid.uuid4()),
                "expected_experience_revision": view["experience_revision"],
                "expected_campaign_revision": self.state()["revision"], **fields}

    def save(self, action, body=None, **fields):
        body = body or self.body(**fields)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            result = experience.mutate(self.db, self.state(), action, body)
            self.assertTrue(self.db.in_transaction, "helper must leave commit ownership with caller")
            self.db.commit()
            return result
        except BaseException:
            self.db.rollback()
            raise

    def advance_fixture(self, number):
        self.db.execute("BEGIN IMMEDIATE")
        self.db.execute("UPDATE hike_day SET status='completed' WHERE status='active'")
        self.db.execute("UPDATE campaign SET revision=revision+1,next_day_number=?", (number,))
        self.db.execute("INSERT INTO hike_day VALUES(?,?,'active')", (number, f"day-{number:03}"))
        self.db.commit()

    def test_schema_and_get_are_noncommitting_and_future_reads_nonmutating(self):
        self.assertFalse(self.view()["eligibility"]["eligible"])
        before = self.db.total_changes
        self.assertFalse(self.view("day-004")["eligibility"]["current_day"])
        self.assertEqual(before, self.db.total_changes)
        self.assertEqual(4, self.db.execute("SELECT COUNT(*) FROM experience_scenario").fetchone()[0])
        with self.assertRaises(RuntimeError):
            experience.ensure_schema(self.db, 4)
        with self.assertRaises(RuntimeError):
            experience.mutate(self.db, self.state(), "preparation", self.body(reviewed_dossier=True))

    def test_units_unknowns_targets_and_nonwalking_observations(self):
        self.save("assignment", activity_category="walking", distance=1, distance_unit="mi", duration_minutes=20,
                  activity_date="2026-10-01", timezone="UTC")
        self.save("workout", distance=None, duration_minutes=None)
        self.assertIsNone(self.view()["actual_totals"]["distance_meters"])
        self.save("workout", distance=100, distance_unit="km", duration_minutes=30, purpose="other_activity")
        self.assertFalse(self.view()["eligibility"]["walking_assignment_met"])
        self.save("workout", distance=1.609344, distance_unit="km", duration_minutes=20,
                  activity_date="2026-10-02", timezone="America/Los_Angeles")
        current = self.view()
        self.assertTrue(current["eligibility"]["walking_assignment_met"])
        self.assertAlmostEqual(1609.344, current["walking_totals"]["distance_meters"])
        self.assertEqual(1, current["actual_totals"]["distance_unknown_count"])
        self.assertEqual(1, current["actual_totals"]["duration_unknown_count"])
        self.assertEqual("UTC", current["assignment"]["timezone"])
        self.assertEqual("America/Los_Angeles", current["workouts"][0]["timezone"])
        self.assertEqual("day-001", current["current_day_id"])
        self.assertFalse(current["eligibility"]["eligible"], "activity alone cannot finish story/journal")

    def test_recovery_participation_does_not_create_activity(self):
        self.save("assignment", activity_category="recovery", notes="My planned recovery day")
        self.save("preparation", reviewed_dossier=True)
        self.save("decision", deferred=True, acknowledged=True)
        self.save("journal", text="", acknowledge_empty=True, expected_journal_revision=0)
        current = self.view()
        self.assertTrue(current["eligibility"]["eligible"])
        self.assertFalse(current["eligibility"]["walking_assignment_met"])
        self.assertIsNone(current["actual_totals"]["distance_meters"])
        self.assertEqual(0, current["workout_count"])
        self.assertEqual(0, self.db.execute("SELECT revision FROM campaign").fetchone()[0])

    def test_story_only_affects_fiction_and_free_recovery_survives_depletion(self):
        self.save("assignment", activity_category="walking", distance=5, distance_unit="mi")
        original = self.view()["assignment"]
        self.save("decision", option_id="ask", acknowledged=True)
        self.assertEqual(original, self.view()["assignment"])
        self.assertEqual(4, self.view()["resources"]["planning_tokens"])
        self.assertEqual(0, self.view()["workout_count"])
        for number, option in ((2,"organize"),(3,"discuss")):
            self.advance_fixture(number)
            self.save("decision", body={**self.body(), "day_id": f"day-{number:03}", "option_id": option, "acknowledged": True})
        self.assertEqual(0, self.view("day-003")["resources"]["planning_tokens"])
        self.advance_fixture(4)
        with self.assertRaises(experience.ExperienceError) as blocked:
            self.save("decision", body={**self.body(), "day_id":"day-004", "option_id":"discussion", "acknowledged":True})
        self.assertEqual(409, blocked.exception.status)
        self.save("decision", body={**self.body(), "day_id":"day-004", "option_id":"compare", "acknowledged":True})
        self.assertEqual(0, self.view("day-004")["resources"]["planning_tokens"])

    def test_replay_lost_ack_and_cross_action_key_reuse(self):
        body = self.body(activity_category="walking", distance=0, distance_unit="mi")
        first = self.save("assignment", body)
        replay = self.save("assignment", body)
        self.assertTrue(replay["replayed"])
        self.assertEqual(first["receipt"], replay["receipt"])
        self.assertEqual(1, self.db.execute("SELECT COUNT(*) FROM experience_assignment").fetchone()[0])
        self.assertEqual(first["receipt"], experience.lookup_operation(self.db, self.state(), body["operation_id"])["receipt"])
        with self.assertRaises(experience.ExperienceError) as changed:
            self.save("assignment", {**body, "distance": 1})
        self.assertEqual(409, changed.exception.status)
        self.save("preparation", reviewed_dossier=True)
        later = self.save("assignment", body)
        self.assertEqual(1, later["receipt"]["resulting_experience_revision"])
        self.assertEqual(2, later["experience"]["experience_revision"])

    def test_stale_tabs_journal_revisions_and_historical_immutability(self):
        stale = self.body(activity_category="walking", distance=2, distance_unit="km")
        self.save("assignment", activity_category="walking", distance=1, distance_unit="mi")
        with self.assertRaises(experience.ExperienceError) as conflict:
            self.save("assignment", stale)
        self.assertEqual(409, conflict.exception.status)
        self.save("assignment", activity_category="walking", distance=2, distance_unit="mi")
        self.assertEqual(2, self.db.execute("SELECT COUNT(*) FROM experience_assignment").fetchone()[0])
        self.save("journal", text="Original reflection", expected_journal_revision=0)
        with self.assertRaises(experience.ExperienceError):
            self.save("journal", text="Stale replacement", expected_journal_revision=0)
        self.save("journal", text="Reviewed reflection", expected_journal_revision=1)
        self.assertEqual("Original reflection", self.db.execute("SELECT text FROM experience_journal WHERE revision=1").fetchone()[0])
        self.advance_fixture(2)
        with self.assertRaises(experience.ExperienceError) as historical:
            self.save("journal", text="Rewritten old day", expected_journal_revision=2)
        self.assertEqual(409, historical.exception.status)
        self.assertEqual("Reviewed reflection", self.view()["journal"]["text"])

    def test_caller_rollback_and_restart_preserve_only_committed_records(self):
        body = self.body(activity_category="walking", duration_minutes=10)
        self.db.execute("BEGIN IMMEDIATE")
        experience.mutate(self.db, self.state(), "assignment", body)
        self.db.rollback()
        self.assertIsNone(self.view()["assignment"])
        self.assertIsNone(experience.lookup_operation(self.db, self.state(), body["operation_id"]))
        self.save("assignment", body)
        self.db.close()
        self.db = sqlite3.connect(self.path, isolation_level=None)
        self.db.execute("PRAGMA foreign_keys=ON")
        self.assertEqual(10, self.view()["assignment"]["duration_minutes"])
        self.assertEqual("ok", self.db.execute("PRAGMA integrity_check").fetchone()[0])
        self.assertEqual([], self.db.execute("PRAGMA foreign_key_check").fetchall())

    def test_payload_bounds_and_domain_authority(self):
        cases = [("workout", {"distance": -1, "distance_unit":"mi"}),
                 ("workout", {"distance":float("nan"), "distance_unit":"km"}),
                 ("workout", {"duration_minutes":True}),
                 ("workout", {"distance":1}),
                 ("workout", {"next_day_number":99}),
                 ("assignment", {"activity_category":"recovery", "distance":1,"distance_unit":"mi"}),
                 ("assignment", {"activity_category":"walking", "notes":"x"*2001}),
                 ("assignment", {"activity_category":"walking", "activity_date":"2026-02-30"}),
                 ("decision", {"option_id":"invented", "acknowledged":True}),
                 ("decision", {"option_id":"compare", "acknowledged":False}),
                 ("journal", {"text":"", "expected_journal_revision":0})]
        for action, values in cases:
            with self.subTest(action=action,values=values):
                with self.assertRaises(experience.ExperienceError):
                    self.save(action, **values)
        self.assertEqual(0, self.view()["experience_revision"])
        self.assertEqual(0, self.db.execute("SELECT COUNT(*) FROM experience_receipt").fetchone()[0])

    def test_content_is_pinned_and_detects_corruption(self):
        before = self.view()["scenario"]
        self.assertEqual(before, self.view()["scenario"])
        self.db.execute("BEGIN IMMEDIATE")
        experience.ensure_schema(self.db, 4)
        self.db.commit()
        self.assertEqual(before, self.view()["scenario"])
        self.db.execute("UPDATE experience_scenario SET payload_json='{}' WHERE day_id='day-001'")
        with self.assertRaises(experience.ExperienceError) as broken:
            self.view()
        self.assertEqual(503, broken.exception.status)

    def test_competing_writers_have_one_effect_and_explicit_stale_conflict(self):
        first = self.body(reviewed_dossier=True)
        second = {**first, "operation_id": str(uuid.uuid4())}
        other = sqlite3.connect(self.path, isolation_level=None, timeout=0.01)
        other.execute("PRAGMA foreign_keys=ON")
        try:
            self.db.execute("BEGIN IMMEDIATE")
            experience.mutate(self.db, self.state(), "preparation", first)
            with self.assertRaises(sqlite3.OperationalError):
                other.execute("BEGIN IMMEDIATE")
            self.db.commit()
            other.execute("BEGIN IMMEDIATE")
            with self.assertRaises(experience.ExperienceError) as stale:
                experience.mutate(other, self.state(), "preparation", second)
            self.assertEqual(409, stale.exception.status)
            other.rollback()
            self.assertEqual(1, self.db.execute("SELECT COUNT(*) FROM experience_receipt").fetchone()[0])
        finally:
            if other.in_transaction:
                other.rollback()
            other.close()


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExperienceTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"passed": result.wasSuccessful(), "tests_run": result.testsRun,
              "failures": len(result.failures), "errors": len(result.errors),
              "personal_database_used": False, "scope": "domain and caller-owned transaction tests only; HTTP/UI integration not assessed here",
              "partial_control_evidence": ["C04.02","C04.03","C04.07","C06.03","C08.10","C11.11","C18.09","C18.10"],
              "all_3720_controls_verified": False}
    (WORK / "experience_test_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    raise SystemExit(0 if result.wasSuccessful() else 1)
