import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import uuid

WORK = Path(__file__).resolve().parent
APP = WORK.parent / "app"
sys.path.insert(0, str(APP))
def load(name):
    spec = importlib.util.spec_from_file_location(name, APP / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
history = load("history_tools")
server = load("server")
experience = load("experience")
TEST = WORK / ("history recovery ü " + str(uuid.uuid4()))
ROOT = TEST / "application"
DATA = ROOT / "data"
DATA.mkdir(parents=True)
checks = []
def check(name, condition):
    assert condition, name
    checks.append(name)
def refusal(name, callback):
    try:
        callback()
    except (history.HistoryError, OSError, sqlite3.Error, ValueError, KeyError):
        checks.append(name)
    else:
        raise AssertionError(name)

source_bytes = b'{"fixture_source":true}'
source_sha = hashlib.sha256(source_bytes).hexdigest()
stages = []
for number in range(1, 4):
    ident = f"day-{number:03}"
    paths = {"map_path": f"content/maps/{ident}.svg", "dossier_path": f"content/dossiers/{ident}.html", "geometry_path": f"content/routes/{ident}.geojson"}
    for key, name in paths.items():
        target = ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>' if key == "map_path" else "<html>Fixture dossier</html>" if key == "dossier_path" else '{"type":"Feature","geometry":null}', encoding="utf-8")
    stages.append({"id": ident, "day_number": number, "mile_start": (number-1)*10, "mile_end": number*10, "distance_miles": 10, **paths})
manifest = {"metadata": {"route_release": "fixture-" + source_sha[:12], "centerline_sha256": source_sha}, "stages": stages}
(ROOT / "content" / "itinerary.json").write_text(json.dumps(manifest), encoding="utf-8")
SOURCES = ROOT / "content" / "sources"
SOURCES.mkdir()
(SOURCES / "centerline_batch_000.json.gz").write_bytes(gzip.compress(source_bytes))
(SOURCES / "source_manifest.json").write_text(json.dumps({"downloads": [{"file": "centerline_batch_000.json", "sha256": source_sha}]}), encoding="utf-8")
service = server.Service(ROOT.resolve(), DATA.resolve(), 8766, str(uuid.uuid4()), str(uuid.uuid4()))
def save_experience(action, **fields):
    campaign_state = service.state()
    db = service.connect()
    try:
        db.execute("BEGIN IMMEDIATE")
        experience.ensure_schema(db, len(stages))
        revision = db.execute("SELECT revision FROM experience_state").fetchone()[0]
        body = {"day_id": campaign_state["current_day_id"], "operation_id": str(uuid.uuid4()),
                "expected_experience_revision": revision, "expected_campaign_revision": campaign_state["revision"], **fields}
        result = experience.mutate(db, campaign_state, action, body)
        db.commit()
        return result
    finally:
        db.close()
def prepare_day():
    save_experience("assignment", activity_category="walking", title="Synthetic accepted assignment", duration_minutes=30, distance=2, distance_unit="mi", notes="Synthetic assignment version 1")
    save_experience("assignment", activity_category="walking", title="Synthetic revised assignment", duration_minutes=25, distance=1.5, distance_unit="mi", notes="Synthetic assignment version 2")
    save_experience("workout", distance=1.5, distance_unit="mi", duration_minutes=25, purpose="walking", notes="Synthetic manual activity note", activity_date="2026-10-01", timezone="UTC")
    save_experience("preparation", reviewed_dossier=True)
    save_experience("decision", option_id="compare", deferred=False, acknowledged=True)
    save_experience("journal", text="Synthetic first private reflection", expected_journal_revision=0, acknowledge_empty=False)
    save_experience("journal", text="Synthetic second private reflection", expected_journal_revision=1, acknowledge_empty=False)
prepare_day()
wal_holder = sqlite3.connect(DATA / "hike.sqlite")
wal_holder.execute("SELECT campaign_id FROM campaign").fetchone()
try:
    first = service.complete({"day_id": "day-001", "expected_revision": 0, "operation_id": str(uuid.uuid4())})
    check("fixture has committed Day 1 and live WAL journal", first["state"]["revision"] == 1 and (DATA / "hike.sqlite-wal").is_file())
    db_before = service.state()
    exported = history.export_history(ROOT, DATA, TEST / "private-history.json")
    payload = json.loads((TEST / "private-history.json").read_text())
    check("JSON export contains committed chronology and pointer", payload["state"]["revision"] == 1 and payload["state"]["next_day_number"] == 2 and len(payload["completions"]) == 1 and len(payload["runs"]) == 1)
    check("private export omits authentication and instance fields", not any(secret in (TEST / "private-history.json").read_text() for secret in (service.nonce, service.instance_id, "instance_id", "receipt_json")))
    history.export_history(ROOT, DATA, TEST / "private-history.jsonl", "jsonl")
    lines = [json.loads(line) for line in (TEST / "private-history.jsonl").read_text().splitlines()]
    check("JSONL export has typed metadata day completion and run records", {"metadata", "day", "completion", "run"} <= {line["type"] for line in lines})
    check("export retains all immutable assignment and reflection versions", len(payload["experience"]["assignments"]) == 2 and len(payload["experience"]["journal_revisions"]) == 2 and payload["experience"]["journal_revisions"][0]["text"] == "Synthetic first private reflection" and payload["experience"]["journal_revisions"][1]["text"] == "Synthetic second private reflection")
    check("export separates manual activity fictional consequences and preparation", len(payload["experience"]["workouts"]) == 1 and len(payload["experience"]["preparation"]) == 1 and len(payload["experience"]["decisions"]) == 1 and len(payload["experience"]["resources"]) == 2 and payload["experience"]["workouts"][0]["source"] == "manual_self_report")
    check("experience receipt export contains metadata without arbitrary receipt JSON", len(payload["experience"]["receipts"]) == 7 and all("receipt_json" not in row and "result" in row and "payload_sha256" in row for row in payload["experience"]["receipts"]))
    check("export retains every checksummed authored scenario snapshot", len(payload["experience"]["scenario_snapshots"]) == 3 and all("payload" in row and "payload_json" not in row and row["payload"]["classification"] == "fictional" for row in payload["experience"]["scenario_snapshots"]))
    check("export does not modify authoritative state", service.state() == db_before)
    refusal("existing export cannot be overwritten", lambda: history.export_history(ROOT, DATA, TEST / "private-history.json"))
    refusal("export cannot be written inside active data", lambda: history.export_history(ROOT, DATA, DATA / "export.json"))
    b1 = history.create_backup(ROOT, DATA, TEST / "backup-one")
    check("online SQLite snapshot includes uncheckpointed commit", b1["state"]["revision"] == 1 and (TEST / "backup-one" / "backup.json").is_file() and not (TEST / "backup-one" / "hike.sqlite-wal").exists())
    valid_manifest_bytes = (TEST / "backup-one" / "backup.json").read_bytes()
    refusal("interrupted backup preserves previous usable backup", lambda: history.create_backup(ROOT, DATA, TEST / "interrupted-backup", timeout_seconds=0))
    check("interrupted backup publishes no success directory", not (TEST / "interrupted-backup").exists() and (TEST / "backup-one" / "backup.json").read_bytes() == valid_manifest_bytes)
    snapshot_map = TEST / "backup-one" / stages[0]["map_path"]
    snapshot_map_bytes = snapshot_map.read_bytes()
    snapshot_map.write_bytes(snapshot_map_bytes + b"<!-- damaged snapshot -->")
    refusal("restore rejects corrupt backup artifact", lambda: history.restore_backup(ROOT, TEST / "backup-one", TEST / "corrupt-artifact-restore"))
    snapshot_map.write_bytes(snapshot_map_bytes)
    wrong_manifest = json.loads(valid_manifest_bytes)
    wrong_manifest["state"]["campaign_id"] = str(uuid.uuid4())
    (TEST / "backup-one" / "backup.json").write_text(json.dumps(wrong_manifest), encoding="utf-8")
    refusal("restore rejects another campaign manifest", lambda: history.restore_backup(ROOT, TEST / "backup-one", TEST / "foreign-campaign-restore"))
    (TEST / "backup-one" / "backup.json").write_bytes(valid_manifest_bytes)
    prepare_day()
    service.complete({"day_id": "day-002", "expected_revision": 1, "operation_id": str(uuid.uuid4())})
    check("live progress can continue independently of backup", service.state()["revision"] == 2 and json.loads((TEST / "backup-one" / "backup.json").read_text())["state"]["revision"] == 1)
    restored = history.restore_backup(ROOT, TEST / "backup-one", TEST / "restored-data")
    check("restore reproduces backup campaign revision and pointer", restored["state"]["campaign_id"] == service.state()["campaign_id"] and restored["state"]["revision"] == 1 and restored["state"]["next_day_number"] == 2 and restored["source_checksums_verified"])
    resumed = server.Service(ROOT.resolve(), (TEST / "restored-data").resolve(), 8766, str(uuid.uuid4()), str(uuid.uuid4()))
    check("application opens restored state at the original unfinished section", resumed.state()["revision"] == 1 and resumed.state()["current_day_id"] == "day-002" and resumed.state()["run_count"] == 2)
    recovered = history.export_history(ROOT, TEST / "restored-data", TEST / "recovered-history.json")
    recovered_payload = json.loads((TEST / "recovered-history.json").read_text())
    check("restore preserves domain history notes all revisions and receipts", recovered_payload["experience"] == payload["experience"] and recovered["state"]["experience_revision"] == 7)
    resumed.finish("closed")
    refusal("restore refuses the active nonempty data directory", lambda: history.restore_backup(ROOT, TEST / "backup-one", DATA))
    refusal("restore refuses an existing restored directory", lambda: history.restore_backup(ROOT, TEST / "backup-one", TEST / "restored-data"))
    empty = TEST / "empty-existing"
    empty.mkdir()
    refusal("restore refuses even an existing empty destination", lambda: history.restore_backup(ROOT, TEST / "backup-one", empty))
    refusal("backup destination cannot be reused", lambda: history.create_backup(ROOT, DATA, TEST / "backup-one"))
    changed_map = ROOT / stages[0]["map_path"]
    original_map = changed_map.read_bytes()
    changed_map.write_bytes(original_map + b"<!--changed-->")
    refusal("restore rejects target content that differs from snapshot", lambda: history.restore_backup(ROOT, TEST / "backup-one", TEST / "mismatched-content"))
    changed_map.write_bytes(original_map)
    archive = SOURCES / "centerline_batch_000.json.gz"
    archive_original = archive.read_bytes()
    archive.write_bytes(gzip.compress(b"wrong source"))
    refusal("backup rejects source archive checksum mismatch", lambda: history.create_backup(ROOT, DATA, TEST / "bad-source-backup"))
    refusal("restore rejects target source archive checksum mismatch", lambda: history.restore_backup(ROOT, TEST / "backup-one", TEST / "bad-source-restore"))
    archive.write_bytes(archive_original)
    backup_db = TEST / "backup-one" / "hike.sqlite"
    original_db = backup_db.read_bytes()
    backup_db.write_bytes(original_db[:256])
    refusal("restore rejects a damaged backup database before publication", lambda: history.restore_backup(ROOT, TEST / "backup-one", TEST / "corrupt-restore"))
    backup_db.write_bytes(original_db)
    db = sqlite3.connect(DATA / "hike.sqlite")
    db.execute("PRAGMA user_version=99")
    db.close()
    refusal("unsupported schema blocks export", lambda: history.export_history(ROOT, DATA, TEST / "unsupported.json"))
    refusal("unsupported schema blocks backup", lambda: history.create_backup(ROOT, DATA, TEST / "unsupported-backup"))
    db = sqlite3.connect(DATA / "hike.sqlite")
    db.execute("PRAGMA user_version=1")
    db.execute("UPDATE campaign SET revision=9")
    db.commit()
    db.close()
    refusal("inconsistent campaign revision blocks export", lambda: history.export_history(ROOT, DATA, TEST / "bad-revision.json"))
    db = sqlite3.connect(DATA / "hike.sqlite")
    db.execute("UPDATE campaign SET revision=2")
    db.commit()
    db.close()
    missing = TEST / "missing-data"
    refusal("missing database never creates an empty campaign", lambda: history.export_history(ROOT, missing, TEST / "missing.json"))
    check("failed recoveries publish no new authoritative directories", not any((TEST / name).exists() for name in ("mismatched-content", "bad-source-restore", "corrupt-restore")))
    check("original live history remains at Day 3 after recovery refusals", service.state()["revision"] == 2 and service.state()["current_day_id"] == "day-003")
    result = {"passed": True, "check_count": len(checks), "checks": checks, "fixture_path": str(TEST), "real_application_data_mutated": False}
    (WORK / "history_tools_test_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
finally:
    wal_holder.close()
    service.finish("closed")
