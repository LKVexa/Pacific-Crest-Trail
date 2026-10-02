"""Real source-map checks; deliberately reseal misaligned temporary SVG copies."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("satellite_verifier", ROOT / "scripts/Verify-Satellite-Maps.py")
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


class SatelliteVerifierTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="satellite-verifier-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        publication = json.loads((ROOT / "content/satellite.json").read_bytes())
        self.row = deepcopy(next(r for r in publication["days"] if r["day_id"] == "day-001"))
        itinerary = json.loads((ROOT / "content/itinerary.json").read_bytes())
        self.stage = next(s for s in itinerary["stages"] if s["id"] == "day-001")
        self.frozen = json.loads((ROOT / "tests/fixtures/topography_baseline.json").read_bytes())["days"]["day-001"]
        self.service = json.loads((ROOT / publication["sources"][0]["metadata_path"]).read_bytes())
        names = {self.row["map_path"], self.row["baseline_path"], self.stage["geometry_path"]}
        for tile in self.row["tiles"]:
            names.update((tile["path"], tile["metadata_path"]))
        for name in names:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)

    def inspect(self):
        return V.verify_day(self.root, self.row, self.frozen, self.stage, self.service)

    def save_svg(self, svg):
        raw = ET.tostring(svg, encoding="utf-8") + b"\n"
        (self.root / self.row["map_path"]).write_bytes(raw)
        self.row["published_map_sha256"] = V.sha(raw)
        self.row["map_revision"] = V.sha(raw)[:16]

    def assert_failure(self, name, result):
        self.assertFalse(result["passed"])
        self.assertTrue(any(name in message for message in result["failures"]), result["failures"])

    def test_real_source_tiles_preserve_original_and_register(self):
        result = self.inspect()
        self.assertTrue(result["passed"], result["failures"])
        self.assertIn("complete_plot_tile_union", result["checks"])
        self.assertIn("original_checkpoint_overlay_geometry", result["checks"])
        self.assertTrue(all(t["true_maximum_error_pixels"] < .25 for t in result["tiles"]))

    def test_shifted_embedded_raster_rejected_after_checksum_update(self):
        svg = ET.parse(self.root / self.row["map_path"]).getroot()
        image = next(e for e in svg.iter() if e.get("id") == "satellite-tile-1")
        image.set("x", str(float(image.get("x")) + 8))
        self.save_svg(svg)
        self.assert_failure("tile_1_geographic_image_placement", self.inspect())

    def test_shifted_slot_clip_rejected_after_checksum_update(self):
        svg = ET.parse(self.root / self.row["map_path"]).getroot()
        rect = svg.find("svg:defs/svg:clipPath[@id='imagery-slot-1']/svg:rect", V.NS)
        rect.set("y", str(float(rect.get("y")) + 8))
        self.save_svg(svg)
        self.assert_failure("tile_1_geographic_slot_clip", self.inspect())


if __name__ == "__main__":
    unittest.main(verbosity=2)
