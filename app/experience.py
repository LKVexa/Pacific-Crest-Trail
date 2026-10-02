"""Additive local experience records; callers own SQLite transactions and commits.

Physical observations, accepted assignments, authored fiction and reflections have
separate records. No fictional effect can write an assignment or workout. This is
a bounded release implementation, not evidence that all acceptance controls pass.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
import uuid
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

VERSION = 1
RULES_VERSION = "trail-experience-1"
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
DAY = re.compile(r"^day-([0-9]{3})$")
COMMON = {"day_id", "operation_id", "expected_experience_revision", "expected_campaign_revision"}
INITIAL_TOKENS = 6


class ExperienceError(Exception):
    def __init__(self, status, code, message):
        super().__init__(message)
        self.status, self.code, self.message = status, code, message


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _fail(code, message, status=400):
    raise ExperienceError(status, code, message)


def ensure_schema(db, day_count=266):
    """Call during backed-up startup migration, inside a caller-owned transaction.

    Deliberately avoids executescript, which would implicitly commit its caller.
    Does not change the main application's PRAGMA user_version.
    """
    if not db.in_transaction:
        raise RuntimeError("Experience schema installation requires a caller-owned transaction.")
    if isinstance(day_count, bool) or not isinstance(day_count, int) or not 1 <= day_count <= 999:
        raise ValueError("The authored experience supports 1-999 numbered daily sections.")
    db.execute("CREATE TABLE IF NOT EXISTS experience_schema (singleton INTEGER PRIMARY KEY CHECK(singleton=1), version INTEGER NOT NULL)")
    row = db.execute("SELECT version FROM experience_schema WHERE singleton=1").fetchone()
    if row is not None and row[0] != VERSION:
        _fail("experience_schema_unsupported", "Preserve this database and use a compatible experience module.", 503)
    statements = [
        """CREATE TABLE IF NOT EXISTS experience_state (
          campaign_id TEXT PRIMARY KEY REFERENCES campaign(campaign_id),
          revision INTEGER NOT NULL CHECK(revision>=0), rules_version TEXT NOT NULL)""",
        """CREATE TABLE IF NOT EXISTS experience_scenario (
          campaign_id TEXT NOT NULL REFERENCES campaign(campaign_id), day_id TEXT NOT NULL,
          rules_version TEXT NOT NULL, payload_json TEXT NOT NULL, sha256 TEXT NOT NULL,
          PRIMARY KEY(campaign_id,day_id))""",
        """CREATE TABLE IF NOT EXISTS experience_assignment (
          assignment_id TEXT PRIMARY KEY, campaign_id TEXT NOT NULL REFERENCES campaign(campaign_id),
          day_id TEXT NOT NULL REFERENCES hike_day(day_id), version INTEGER NOT NULL CHECK(version>=1),
          activity_category TEXT NOT NULL CHECK(activity_category IN ('walking','recovery','preparation')),
          title TEXT NOT NULL, duration_minutes REAL CHECK(duration_minutes>=0),
          distance REAL CHECK(distance>=0), distance_unit TEXT CHECK(distance_unit IN ('mi','km')),
          distance_meters REAL CHECK(distance_meters>=0), activity_date TEXT, timezone TEXT,
          notes TEXT NOT NULL, origin TEXT NOT NULL CHECK(origin='user_authored'),
          accepted_at TEXT NOT NULL, operation_id TEXT NOT NULL UNIQUE,
          UNIQUE(campaign_id,day_id,version))""",
        """CREATE TABLE IF NOT EXISTS experience_workout (
          workout_id TEXT PRIMARY KEY, campaign_id TEXT NOT NULL REFERENCES campaign(campaign_id),
          day_id TEXT NOT NULL REFERENCES hike_day(day_id), assignment_id TEXT REFERENCES experience_assignment(assignment_id),
          distance REAL CHECK(distance>=0), distance_unit TEXT CHECK(distance_unit IN ('mi','km')),
          distance_meters REAL CHECK(distance_meters>=0), duration_minutes REAL CHECK(duration_minutes>=0),
          purpose TEXT NOT NULL, notes TEXT NOT NULL, activity_date TEXT, timezone TEXT,
          source TEXT NOT NULL CHECK(source='manual_self_report'),
          recorded_at TEXT NOT NULL, operation_id TEXT NOT NULL UNIQUE)""",
        """CREATE TABLE IF NOT EXISTS experience_preparation (
          campaign_id TEXT NOT NULL REFERENCES campaign(campaign_id), day_id TEXT NOT NULL REFERENCES hike_day(day_id),
          reviewed_at TEXT NOT NULL, content_version TEXT NOT NULL, operation_id TEXT NOT NULL UNIQUE,
          PRIMARY KEY(campaign_id,day_id))""",
        """CREATE TABLE IF NOT EXISTS experience_decision (
          campaign_id TEXT NOT NULL REFERENCES campaign(campaign_id), day_id TEXT NOT NULL REFERENCES hike_day(day_id),
          option_id TEXT, deferred INTEGER NOT NULL CHECK(deferred IN (0,1)),
          scenario_version TEXT NOT NULL, outcome_json TEXT NOT NULL, decided_at TEXT NOT NULL,
          operation_id TEXT NOT NULL UNIQUE, PRIMARY KEY(campaign_id,day_id))""",
        """CREATE TABLE IF NOT EXISTS experience_resource (
          transaction_id TEXT PRIMARY KEY, campaign_id TEXT NOT NULL REFERENCES campaign(campaign_id),
          day_id TEXT NOT NULL REFERENCES hike_day(day_id), operation_id TEXT NOT NULL,
          resource TEXT NOT NULL CHECK(resource IN ('planning_tokens','insight_stamps')), delta INTEGER NOT NULL,
          rule_version TEXT NOT NULL, cause TEXT NOT NULL, recorded_at TEXT NOT NULL,
          UNIQUE(operation_id,resource))""",
        """CREATE TABLE IF NOT EXISTS experience_journal (
          campaign_id TEXT NOT NULL REFERENCES campaign(campaign_id), day_id TEXT NOT NULL REFERENCES hike_day(day_id),
          revision INTEGER NOT NULL CHECK(revision>=1), text TEXT NOT NULL,
          acknowledge_empty INTEGER NOT NULL CHECK(acknowledge_empty IN (0,1)),
          recorded_at TEXT NOT NULL, operation_id TEXT NOT NULL UNIQUE,
          PRIMARY KEY(campaign_id,day_id,revision))""",
        """CREATE TABLE IF NOT EXISTS experience_receipt (
          operation_id TEXT PRIMARY KEY, campaign_id TEXT NOT NULL REFERENCES campaign(campaign_id),
          day_id TEXT NOT NULL REFERENCES hike_day(day_id), action TEXT NOT NULL,
          payload_sha256 TEXT NOT NULL, receipt_json TEXT NOT NULL, committed_at TEXT NOT NULL)""",
    ]
    for statement in statements:
        db.execute(statement)
    db.execute("INSERT OR IGNORE INTO experience_schema VALUES (1,?)", (VERSION,))
    db.execute("INSERT OR IGNORE INTO experience_state SELECT campaign_id,0,? FROM campaign", (RULES_VERSION,))
    for cid, in db.execute("SELECT campaign_id FROM campaign").fetchall():
        for number in range(1, day_count + 1):
            day_id = f"day-{number:03}"
            payload = _json(scenario(day_id))
            db.execute("INSERT OR IGNORE INTO experience_scenario VALUES (?,?,?,?,?)",
                       (cid, day_id, RULES_VERSION, payload, hashlib.sha256(payload.encode("utf-8")).hexdigest()))


def _dict(cursor):
    row = cursor.fetchone()
    return dict(zip([c[0] for c in cursor.description], row)) if row is not None else None


def _all(cursor):
    columns = [c[0] for c in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def _campaign(db, state):
    actual = _dict(db.execute("SELECT campaign_id,revision FROM campaign WHERE singleton=1"))
    if not isinstance(state, dict) or actual is None or state.get("campaign_id") != actual["campaign_id"]:
        _fail("campaign_conflict", "Reload this repository's active campaign.", 409)
    return actual


def _day(state, day_id):
    match = DAY.fullmatch(day_id) if isinstance(day_id, str) else None
    count = state.get("total_days", 0)
    if not match or not isinstance(count, int) or not 1 <= int(match[1]) <= count:
        _fail("invalid_day", "Choose an existing daily section from this itinerary.")
    return day_id


def _text(body, field, limit, default=""):
    value = body.get(field, default)
    if not isinstance(value, str) or len(value) > limit or "\x00" in value:
        _fail("invalid_" + field, f"{field} must be plain text no longer than {limit} characters.")
    return value


def _number(body, field):
    value = body.get(field)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1_000_000 or not math.isfinite(value):
        _fail("invalid_" + field, f"{field} must be a finite nonnegative number or null.")
    return value


def _distance(body):
    value = _number(body, "distance")
    unit = body.get("distance_unit")
    if unit is not None and unit not in ("mi", "km"):
        _fail("invalid_distance_unit", "Use mi or km; unknown distance remains null.")
    if value is not None and unit is None:
        _fail("distance_unit_required", "An entered distance requires an explicit unit.")
    return value, unit, None if value is None else value * (1609.344 if unit == "mi" else 1000)


def _calendar(body):
    value, zone = body.get("activity_date"), body.get("timezone")
    if value is not None:
        if not isinstance(value, str) or len(value) != 10:
            _fail("invalid_activity_date", "Use a date-only YYYY-MM-DD value or null.")
        try:
            if date.fromisoformat(value).isoformat() != value:
                raise ValueError()
        except ValueError:
            _fail("invalid_activity_date", "Use a valid date-only YYYY-MM-DD value.")
    if zone is not None:
        if not isinstance(zone, str) or len(zone) > 100:
            _fail("invalid_timezone", "Use a supported named timezone or null.")
        try:
            ZoneInfo(zone)
        except (ZoneInfoNotFoundError, ValueError):
            _fail("invalid_timezone", "That named timezone is unavailable in this runtime; retain null or choose a supported timezone.")
    return value, zone


def scenario(day_id):
    """Authored hypotheses, not current trail conditions or physical instructions."""
    number = int(DAY.fullmatch(day_id)[1])
    families = [
        ("Route planning", "In this fictional planning exercise, two notes describe the same virtual section. Neither note confirms current trail conditions.",
         "Compare their assumptions before choosing what to carry forward into the story.",
         [("compare", "Compare the two notes", 0, "You identify an assumption to revisit at camp."),
          ("annotate", "Spend a token annotating the plan", 1, "The fictional party receives an annotated route note."),
          ("ask", "Spend two tokens asking the fictional guide", 2, "The guide offers another perspective, without changing real training.")]),
        ("Virtual resupply", "The fictional town offers three planning services. Planning tokens are game counters; no real money or food is purchased.",
         "Compare the listed virtual price with what the option adds; a free choice remains available.",
         [("compare", "Compare your existing inventory notes", 0, "You keep your tokens and clarify a planning priority."),
          ("inventory", "Buy a fictional inventory check for one token", 1, "Your fictional inventory note gains a review stamp."),
          ("organize", "Buy a fictional organizer's help for two tokens", 2, "The fictional party organizes its notes for camp.")]),
        ("Hypothetical weather", "An authored fictional forecast says conditions may change later. This exercise is not a weather report or equipment instruction.",
         "Identify what is assumed, what is unknown, and which information you would need before making a real plan.",
         [("compare", "Record the unknowns and retain your tokens", 0, "The story records your uncertainty without penalizing participation."),
          ("review", "Spend one token reviewing the fictional forecast", 1, "You annotate the forecast's supplied assumptions."),
          ("discuss", "Spend two tokens discussing story alternatives", 2, "The fictional group compares two authored alternatives.")]),
        ("Virtual camp", "Tonight's camp is a fictional narrative endpoint, not a verified campsite. Camp services below affect game counters only.",
         "Reflect on one useful preparation question; virtual distance does not imply you physically visited this place.",
         [("compare", "Use the free camp reflection", 0, "The fictional group shares one reflection at camp."),
          ("notes", "Spend one token organizing camp notes", 1, "Your fictional camp notes receive an organization stamp."),
          ("discussion", "Spend two tokens on an extended fictional discussion", 2, "The group compares priorities without requesting extra exercise.")]),
    ]
    title, assumptions, lesson, choices = families[(number - 1) % len(families)]
    return {"id": f"scenario-{day_id}", "version": RULES_VERSION, "classification": "fictional",
            "title": title, "assumptions": assumptions, "lesson_prompt": lesson,
            "training_reference": "Your accepted user-authored assignment is separate. Story choices never change physical targets.",
            "reflection_prompt": "What did you notice or learn? A deliberate empty reflection is allowed.",
            "defer_allowed": True,
            "options": [{"id": key, "label": label, "cost_planning_tokens": cost, "insight_stamps": 1, "outcome": outcome}
                        for key, label, cost, outcome in choices]}


def _resources(db, campaign_id):
    amounts = {"planning_tokens": INITIAL_TOKENS, "insight_stamps": 0}
    for resource, delta in db.execute("SELECT resource,SUM(delta) FROM experience_resource WHERE campaign_id=? GROUP BY resource", (campaign_id,)):
        amounts[resource] += delta
    return {"classification": "fictional", **amounts}


def _saved_scenario(db, campaign_id, day_id):
    row = db.execute("SELECT rules_version,payload_json,sha256 FROM experience_scenario WHERE campaign_id=? AND day_id=?", (campaign_id, day_id)).fetchone()
    if row is None or row[0] != RULES_VERSION or hashlib.sha256(row[1].encode("utf-8")).hexdigest() != row[2]:
        _fail("scenario_integrity_failure", "The pinned authored scenario needs supported content recovery.", 503)
    return json.loads(row[1])


def get_experience(db, campaign_state, day_id):
    """Read-only; root should call under its coherent read transaction."""
    campaign = _campaign(db, campaign_state)
    day_id = _day(campaign_state, day_id)
    cid = campaign["campaign_id"]
    row = db.execute("SELECT revision,rules_version FROM experience_state WHERE campaign_id=?", (cid,)).fetchone()
    if row is None or row[1] != RULES_VERSION:
        _fail("experience_not_ready", "The experience schema or authored rules require supported startup reconciliation.", 503)
    assignment = _dict(db.execute("SELECT * FROM experience_assignment WHERE campaign_id=? AND day_id=? ORDER BY version DESC LIMIT 1", (cid, day_id)))
    workouts = _all(db.execute("SELECT * FROM experience_workout WHERE campaign_id=? AND day_id=? ORDER BY recorded_at DESC,workout_id DESC LIMIT 200", (cid, day_id)))
    totals = db.execute("SELECT COUNT(*),SUM(distance_meters),SUM(duration_minutes),SUM(CASE WHEN distance_meters IS NULL THEN 1 ELSE 0 END),SUM(CASE WHEN duration_minutes IS NULL THEN 1 ELSE 0 END) FROM experience_workout WHERE campaign_id=? AND day_id=?", (cid, day_id)).fetchone()
    walking = db.execute("SELECT SUM(distance_meters),SUM(duration_minutes),SUM(CASE WHEN distance_meters>0 OR duration_minutes>0 THEN 1 ELSE 0 END) FROM experience_workout WHERE campaign_id=? AND day_id=? AND purpose='walking'", (cid, day_id)).fetchone()
    preparation = _dict(db.execute("SELECT reviewed_at,content_version FROM experience_preparation WHERE campaign_id=? AND day_id=?", (cid, day_id)))
    decision = _dict(db.execute("SELECT option_id,deferred,scenario_version,outcome_json,decided_at FROM experience_decision WHERE campaign_id=? AND day_id=?", (cid, day_id)))
    if decision:
        decision["deferred"] = bool(decision["deferred"])
        decision["outcome"] = json.loads(decision.pop("outcome_json"))
    journal = _dict(db.execute("SELECT revision,text,acknowledge_empty,recorded_at FROM experience_journal WHERE campaign_id=? AND day_id=? ORDER BY revision DESC LIMIT 1", (cid, day_id)))
    if journal:
        journal["acknowledge_empty"] = bool(journal["acknowledge_empty"])
    active = db.execute("SELECT day_id FROM hike_day WHERE status='active'").fetchone()
    current = active is not None and active[0] == day_id
    physical = (walking[2] or 0) > 0
    targets_met = physical
    if assignment and assignment["activity_category"] == "walking":
        if assignment["distance_meters"] is not None:
            targets_met = targets_met and walking[0] is not None and walking[0] + 1e-8 >= assignment["distance_meters"]
        if assignment["duration_minutes"] is not None:
            targets_met = targets_met and walking[1] is not None and walking[1] + 1e-8 >= assignment["duration_minutes"]
    else:
        targets_met = physical and assignment is None
    # Reviewing the dossier is explicit preparation participation. It is a story
    # alternative, never an assertion that a physical assignment was completed.
    participation = preparation is not None or targets_met
    reflection = journal is not None and (bool(journal["text"].strip()) or journal["acknowledge_empty"])
    missing = []
    if not current:
        missing.append("This is not the current unfinished day.")
    if not participation:
        missing.append("Review this dossier as preparation or record activity satisfying your accepted walking assignment.")
    if decision is None:
        missing.append("Choose a fictional story option or explicitly acknowledge deferral.")
    if not reflection:
        missing.append("Save a camp reflection or explicitly acknowledge an empty reflection.")
    return {"day_id": day_id, "campaign_id": cid, "campaign_revision": campaign["revision"],
            "current_day_id": active[0] if active else None, "experience_revision": row[0], "rules_version": row[1],
            "assignment": assignment, "workouts": workouts, "workout_count": totals[0], "more_workouts": totals[0] > len(workouts),
            "actual_totals": {"source": "manual_self_report", "distance_meters": totals[1], "duration_minutes": totals[2],
                              "distance_unknown_count": totals[3] or 0, "duration_unknown_count": totals[4] or 0,
                              "quantity_semantics": "Known subtotals; unknown records are excluded, never filled with zero or estimated movement.",
                              "note": "Unknown quantities remain null. Application use and preparation create no walking distance."},
            "walking_totals": {"distance_meters": walking[0], "duration_minutes": walking[1]},
            "preparation": preparation, "decision": decision, "journal": journal,
            "scenario": _saved_scenario(db, cid, day_id), "resources": _resources(db, cid),
            "eligibility": {"eligible": not missing, "current_day": current, "participation_met": participation,
                            "walking_assignment_met": bool(targets_met), "decision_met": decision is not None,
                            "journal_met": bool(reflection), "missing": missing}}


def require_eligible(db, campaign_state, day_id):
    result = get_experience(db, campaign_state, day_id)
    if not result["eligibility"]["eligible"]:
        _fail("day_requirements_unmet", " ".join(result["eligibility"]["missing"]), 409)
    return result


def lookup_operation(db, campaign_state, operation_id):
    """Read a durable receipt; returns None when the identity is not an experience action."""
    if not isinstance(operation_id, str) or not ID.fullmatch(operation_id):
        _fail("invalid_operation_id", "Use a valid operation identity.")
    campaign = _campaign(db, campaign_state)
    saved = _dict(db.execute("SELECT * FROM experience_receipt WHERE operation_id=?", (operation_id,)))
    if saved is None:
        return None
    if saved["campaign_id"] != campaign["campaign_id"]:
        _fail("operation_campaign_conflict", "That operation belongs to another campaign.", 409)
    return {"ok": True, "operation_id": operation_id, "replayed": True,
            "receipt": json.loads(saved["receipt_json"]), "experience": get_experience(db, campaign_state, saved["day_id"])}


def _validate_payload(action, body):
    permitted = {
        "assignment": {"activity_category", "title", "duration_minutes", "distance", "distance_unit", "activity_date", "timezone", "notes"},
        "workout": {"distance", "distance_unit", "duration_minutes", "purpose", "notes", "activity_date", "timezone"},
        "preparation": {"reviewed_dossier"},
        "decision": {"option_id", "deferred", "acknowledged"},
        "journal": {"text", "expected_journal_revision", "acknowledge_empty"},
    }
    if action not in permitted:
        _fail("unknown_experience_action", "This experience action is unsupported.", 404)
    if not isinstance(body, dict) or not COMMON <= set(body) or set(body) - COMMON - permitted[action]:
        _fail("invalid_experience_schema", "Use the documented fields and both expected revisions for this action.")
    if not isinstance(body["operation_id"], str) or not ID.fullmatch(body["operation_id"]):
        _fail("invalid_operation_id", "Use a stable path-safe operation identity for retries.")
    for field in ("expected_experience_revision", "expected_campaign_revision"):
        if isinstance(body[field], bool) or not isinstance(body[field], int) or body[field] < 0:
            _fail("invalid_revision", "Expected revisions must be nonnegative integers.")
    try:
        payload = _json(body)
    except (TypeError, ValueError):
        _fail("invalid_payload", "Use finite JSON values only.")
    if len(payload.encode("utf-8")) > 16_384:
        _fail("experience_body_too_large", "The experience action exceeds the local body limit.", 413)
    return hashlib.sha256((action + "\n" + payload).encode("utf-8")).hexdigest()


def mutate(db, campaign_state, action, body):
    """Does not begin, commit, roll back or close the caller's connection."""
    if not db.in_transaction:
        raise RuntimeError("Experience writes require caller-owned BEGIN IMMEDIATE.")
    fingerprint = _validate_payload(action, body)
    campaign = _campaign(db, campaign_state)
    day_id = _day(campaign_state, body["day_id"])
    cid, operation = campaign["campaign_id"], body["operation_id"]
    previous = _dict(db.execute("SELECT * FROM experience_receipt WHERE operation_id=?", (operation,)))
    if previous:
        if previous["campaign_id"] != cid or previous["payload_sha256"] != fingerprint:
            _fail("operation_payload_conflict", "This operation identity already belongs to a different action or payload.", 409)
        return {"ok": True, "operation_id": operation, "replayed": True, "receipt": json.loads(previous["receipt_json"]),
                "experience": get_experience(db, campaign_state, day_id)}
    if db.execute("SELECT 1 FROM completion WHERE operation_id=?", (operation,)).fetchone():
        _fail("operation_payload_conflict", "This operation identity already belongs to day completion.", 409)
    current = db.execute("SELECT day_id FROM hike_day WHERE status='active'").fetchone()
    revision = db.execute("SELECT revision FROM experience_state WHERE campaign_id=?", (cid,)).fetchone()
    if current is None or current[0] != day_id or campaign_state.get("current_day_id") != day_id:
        _fail("day_conflict", "Only the current unfinished day accepts new experience writes.", 409)
    if revision is None or body["expected_experience_revision"] != revision[0] or body["expected_campaign_revision"] != campaign["revision"]:
        _fail("experience_revision_conflict", "Reload the saved day and compare your unsaved input before reapplying it.", 409)
    stamp, receipt = _now(), {"operation_id": operation, "action": action, "day_id": day_id, "resulting_experience_revision": revision[0] + 1}
    if action == "assignment":
        category = body.get("activity_category")
        if category not in ("walking", "recovery", "preparation"):
            _fail("invalid_activity_category", "Choose walking, recovery, or preparation for your own assignment.")
        distance, unit, meters = _distance(body)
        duration = _number(body, "duration_minutes")
        if category != "walking" and (distance is not None or duration is not None):
            _fail("nonwalking_physical_target", "Recovery/preparation assignments use descriptive tasks, not walking targets.")
        title, notes = _text(body, "title", 200, "My accepted assignment"), _text(body, "notes", 2000)
        activity_date, zone = _calendar(body)
        version = db.execute("SELECT COALESCE(MAX(version),0)+1 FROM experience_assignment WHERE campaign_id=? AND day_id=?", (cid, day_id)).fetchone()[0]
        assignment_id = "assignment-" + uuid.uuid4().hex
        db.execute("INSERT INTO experience_assignment VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,'user_authored',?,?)",
                   (assignment_id, cid, day_id, version, category, title, duration, distance, unit, meters, activity_date, zone, notes, stamp, operation))
        receipt.update(assignment_id=assignment_id, assignment_version=version)
    elif action == "workout":
        distance, unit, meters = _distance(body)
        duration, notes = _number(body, "duration_minutes"), _text(body, "notes", 2000)
        purpose = body.get("purpose", "walking")
        if purpose not in ("walking", "equipment_practice", "other_activity"):
            _fail("invalid_workout_purpose", "Use walking, equipment_practice, or other_activity.")
        activity_date, zone = _calendar(body)
        assignment = db.execute("SELECT assignment_id FROM experience_assignment WHERE campaign_id=? AND day_id=? ORDER BY version DESC LIMIT 1", (cid, day_id)).fetchone()
        workout_id = "workout-" + uuid.uuid4().hex
        db.execute("INSERT INTO experience_workout VALUES (?,?,?,?,?,?,?,?,?,?,?,?,'manual_self_report',?,?)",
                   (workout_id, cid, day_id, assignment[0] if assignment else None, distance, unit, meters, duration, purpose, notes, activity_date, zone, stamp, operation))
        receipt["workout_id"] = workout_id
    elif action == "preparation":
        if body.get("reviewed_dossier") is not True:
            _fail("preparation_ack_required", "Deliberately confirm that you reviewed this dossier as preparation.")
        if db.execute("SELECT 1 FROM experience_preparation WHERE campaign_id=? AND day_id=?", (cid, day_id)).fetchone():
            _fail("preparation_already_recorded", "This day's preparation review is already saved.", 409)
        db.execute("INSERT INTO experience_preparation VALUES (?,?,?,?,?)", (cid, day_id, stamp, RULES_VERSION, operation))
    elif action == "decision":
        if body.get("acknowledged") is not True:
            _fail("decision_ack_required", "Acknowledge your selected fictional option or deliberate deferral.")
        if db.execute("SELECT 1 FROM experience_decision WHERE campaign_id=? AND day_id=?", (cid, day_id)).fetchone():
            _fail("decision_already_saved", "This day's branch is saved; ordinary edits cannot rewrite established story history.", 409)
        deferred = body.get("deferred", False)
        if not isinstance(deferred, bool):
            _fail("invalid_deferral", "deferred must be true or false.")
        definition = _saved_scenario(db, cid, day_id)
        if deferred:
            if body.get("option_id") is not None:
                _fail("conflicting_decision", "Choose an option or explicitly defer, rather than both.")
            option, outcome = None, {"text": "You deliberately defer this optional fictional scene. No physical targets or resources change.", "classification": "fictional"}
        else:
            option = next((x for x in definition["options"] if x["id"] == body.get("option_id")), None)
            if option is None:
                _fail("invalid_story_option", "Choose one of this saved scenario's authored options.")
            if _resources(db, cid)["planning_tokens"] < option["cost_planning_tokens"]:
                _fail("insufficient_fictional_tokens", "Choose the free option or defer. Extra physical activity is never required.", 409)
            outcome = {"text": option["outcome"], "classification": "fictional"}
            for resource, delta in (("planning_tokens", -option["cost_planning_tokens"]), ("insight_stamps", option["insight_stamps"])):
                db.execute("INSERT INTO experience_resource VALUES (?,?,?,?,?,?,?,?,?)",
                           ("resource-" + uuid.uuid4().hex, cid, day_id, operation, resource, delta, RULES_VERSION, definition["id"] + ":" + option["id"], stamp))
        db.execute("INSERT INTO experience_decision VALUES (?,?,?,?,?,?,?,?)",
                   (cid, day_id, option["id"] if option else None, int(deferred), RULES_VERSION, _json(outcome), stamp, operation))
    elif action == "journal":
        text = _text(body, "text", 8000)
        acknowledged = body.get("acknowledge_empty", False)
        if not isinstance(acknowledged, bool) or not text.strip() and not acknowledged:
            _fail("journal_ack_required", "Write a reflection or deliberately acknowledge an empty reflection.")
        previous_revision = db.execute("SELECT COALESCE(MAX(revision),0) FROM experience_journal WHERE campaign_id=? AND day_id=?", (cid, day_id)).fetchone()[0]
        expected = body.get("expected_journal_revision")
        if isinstance(expected, bool) or not isinstance(expected, int) or expected != previous_revision:
            _fail("journal_revision_conflict", "Compare your reflection with the saved revision before reapplying it.", 409)
        db.execute("INSERT INTO experience_journal VALUES (?,?,?,?,?,?,?)", (cid, day_id, previous_revision + 1, text, int(acknowledged), stamp, operation))
        receipt["journal_revision"] = previous_revision + 1
    db.execute("UPDATE experience_state SET revision=revision+1 WHERE campaign_id=? AND revision=?", (cid, revision[0]))
    db.execute("INSERT INTO experience_receipt VALUES (?,?,?,?,?,?,?)", (operation, cid, day_id, action, fingerprint, _json(receipt), stamp))
    return {"ok": True, "operation_id": operation, "replayed": False, "receipt": receipt,
            "experience": get_experience(db, campaign_state, day_id)}


def publish_scenarios(stages, destination):
    """Publish authored JSON independently from the immutable geographic itinerary."""
    from pathlib import Path
    target = Path(destination)
    value = {"schema_version": VERSION, "rules_version": RULES_VERSION, "classification": "fictional",
             "physical_target_changes": 0, "days": {stage["id"]: scenario(stage["id"]) for stage in stages}}
    raw = (_json(value) + "\n").encode("utf-8")
    staging = target.with_name(target.name + ".staging-" + uuid.uuid4().hex)
    staging.write_bytes(raw)
    if staging.read_bytes() != raw:
        raise OSError("Authored experience package verification failed.")
    staging.replace(target)
    return {"path": str(target), "day_count": len(value["days"]), "sha256": hashlib.sha256(raw).hexdigest(), "rules_version": RULES_VERSION}
