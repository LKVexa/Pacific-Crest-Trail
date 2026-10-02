"""Real-asset mutation tests for the independent geographic map verifier.

Copies one public map/source bundle into a temporary directory. Never changes
published maps, itinerary, private history, installed browser, or network state.
"""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("topographic_verifier", ROOT / "scripts" / "Verify-Topographic-Maps.py")
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class TopographicVerifierTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="topography-verifier-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        publication = json.loads((ROOT / "content" / "topography.json").read_text(encoding="utf-8"))
        self.row = deepcopy(next(r for r in publication["days"] if r["day_id"] == "day-001"))
        itinerary = json.loads((ROOT / "content" / "itinerary.json").read_text(encoding="utf-8"))
        self.stage = deepcopy(next(s for s in itinerary["stages"] if s["id"] == "day-001"))
        frozen = json.loads((ROOT / "tests" / "fixtures" / "topography_baseline.json").read_text(encoding="utf-8"))
        self.frozen = frozen["days"]["day-001"]
        for name in (self.row["map_path"], self.row["baseline_path"], self.row["source_image_path"], self.row["export_metadata_path"], self.stage["geometry_path"]):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)

    def inspect(self):
        return VERIFY.verify_day(self.root, self.row, self.frozen, self.stage)

    def save_svg(self, svg):
        raw = ET.tostring(svg, encoding="utf-8") + b"\n"
        (self.root / self.row["map_path"]).write_bytes(raw)
        # These tests deliberately update the publication checksum: geometric
        # checks must detect wrong placement even when metadata is self-consistent.
        self.row["published_map_sha256"] = VERIFY.sha(raw)

    def svg(self):
        return ET.parse(self.root / self.row["map_path"]).getroot()

    def assert_failure(self, result, name):
        self.assertFalse(result["passed"])
        self.assertTrue(any(name in failure for failure in result["failures"]), result["failures"])

    def test_published_sample_registers_and_preserves_original(self):
        result = self.inspect()
        self.assertTrue(result["passed"], result["failures"])
        self.assertIn("geographic_affine_placement", result["checks"])
        self.assertIn("exact_route_path", result["checks"])

    def test_altered_route_rejected_even_after_hash_update(self):
        svg = self.svg()
        route = VERIFY.route(svg)
        route.set("d", route.get("d") + " L400,400")
        self.save_svg(svg)
        self.assert_failure(self.inspect(), "exact_route_path")

    def test_shifted_raster_rejected_even_after_hash_update(self):
        svg = self.svg()
        image = next(e for e in svg.iter() if e.get("id") == "usgs-topography")
        image.set("x", str(float(image.get("x")) + 12))
        self.save_svg(svg)
        self.assert_failure(self.inspect(), "geographic_affine_placement")

    def test_added_image_transform_rejected(self):
        svg = self.svg()
        image = next(e for e in svg.iter() if e.get("id") == "usgs-topography")
        image.set("transform", "translate(20 10)")
        self.save_svg(svg)
        self.assert_failure(self.inspect(), "affine_raster_sampling")

    def test_moved_checkpoint_rejected_even_after_hash_update(self):
        svg = self.svg()
        start = next(e for e in VERIFY.group(svg, "plot") if VERIFY.local_name(e) == "circle" and e.get("r") == "7")
        start.set("cx", str(float(start.get("cx")) + 4))
        self.save_svg(svg)
        self.assert_failure(self.inspect(), "original_overlay_geometry")

    def test_changed_cached_extent_rejected(self):
        cached_path = self.root / self.row["export_metadata_path"]
        cached = json.loads(cached_path.read_text(encoding="utf-8"))
        cached["response"]["extent"]["xmin"] += .01
        cached_path.write_text(json.dumps(cached), encoding="utf-8")
        self.assert_failure(self.inspect(), "provider_extent")

    def test_changed_original_baseline_cannot_be_resealed(self):
        path = self.root / self.row["baseline_path"]
        svg = ET.parse(path).getroot()
        svg.find("svg:title", VERIFY.NS).text += " changed"
        raw = ET.tostring(svg, encoding="utf-8")
        path.write_bytes(raw)
        self.row["baseline_sha256"] = VERIFY.sha(raw)
        self.assert_failure(self.inspect(), "frozen_original")

    def test_corrupt_png_chunk_crc_rejected(self):
        raw = bytearray((self.root / self.row["source_image_path"]).read_bytes())
        raw[29] ^= 1  # IHDR's CRC, after the complete PNG signature/header.
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            VERIFY.read_png(bytes(raw))


if __name__ == "__main__":
    unittest.main(verbosity=2)
