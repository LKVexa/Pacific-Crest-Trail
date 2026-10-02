"""Public-source location and corruption checks, independent of photo publisher."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('leg_photo_verifier', ROOT / 'scripts' / 'Verify-Leg-Photos.py')
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


class GroundPhotoVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        itinerary = json.loads((ROOT / 'content/itinerary.json').read_text(encoding='utf-8'))
        cls.stages = {s['id']: s for s in itinerary['stages']}
        routes = {i: json.loads((ROOT / s['geometry_path']).read_text(encoding='utf-8'))['geometry']['coordinates'] for i, s in cls.stages.items()}
        cls.index = V.RouteIndex(routes)
        cls.fixture = json.loads((ROOT / 'tests/fixtures/ground_photo_card.json').read_text(encoding='utf-8'))

    def setUp(self):
        self.ident = self.fixture['day_id']
        self.photo = deepcopy(self.fixture['photo'])

    def inspect(self, ident=None):
        ident = ident or self.ident
        return V.verify_photo(ROOT, self.photo, ident, self.stages[ident], self.index, V.PublicSourceReader(ROOT), {}, require_local=False)

    def assert_failure(self, name, result):
        self.assertFalse(result['passed'])
        self.assertTrue(any(name in f for f in result['failures']), result['failures'])

    def test_real_source_geotag_and_nearest_leg(self):
        result = self.inspect()
        self.assertTrue(result['passed'], result['failures'])
        self.assertIn('globally_nearest_leg', result['checks'])
        self.assertIn('provider_geotag_evidence', result['checks'])

    def test_changed_geotag_cannot_keep_original_source_proof(self):
        self.photo['latitude'] += .0005
        self.assert_failure('provider_geotag_evidence', self.inspect())

    def test_self_consistent_mile_cannot_move_geographic_route_fraction(self):
        assignment = self.photo['assignment']
        assignment['route_fraction'] = min(.9, assignment['route_fraction'] + .1)
        stage = self.stages[self.ident]
        self.photo['route_mile'] = stage['mile_start'] + stage['distance_miles'] * assignment['route_fraction']
        self.assert_failure('ground_along_route_location', self.inspect())

    def test_reassigning_ground_photo_to_farther_leg_is_rejected(self):
        other = self.stages[self.ident]['next_day_id']
        point = self.photo['longitude'], self.photo['latitude']
        offset, fraction = self.index.assigned(point, other)
        self.photo['assignment'].update(day_id=other, distance_meters=offset, route_fraction=fraction)
        self.photo['distance_to_section_meters'] = offset
        stage = self.stages[other]
        self.photo['route_mile'] = stage['mile_start'] + stage['distance_miles'] * fraction
        self.assert_failure('globally_nearest_leg', self.inspect(other))

    def test_source_metadata_checksum_mismatch_is_rejected(self):
        self.photo['provenance']['image_metadata_source_sha256'] = '0' * 64
        self.assert_failure('checksum mismatch', self.inspect())

    def test_changed_compressed_archive_header_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='photo-source-verifier-') as temporary:
            root = Path(temporary)
            name = self.photo['provenance']['geotag_source_path']
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            raw = bytearray((ROOT / name).read_bytes())
            raw[4] ^= 1  # Header metadata changes without changing provider JSON.
            target.write_bytes(raw)
            manifest = root / 'content/sources/visual_curation/manifest.json'
            shutil.copyfile(ROOT / 'content/sources/visual_curation/manifest.json', manifest)
            reader = V.PublicSourceReader(root)
            with self.assertRaisesRegex(ValueError, 'not pinned'):
                reader.read(name, self.photo['provenance']['geotag_source_sha256'])


class GroundCacheVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not hasattr(GroundPhotoVerifierTests, 'index'):
            GroundPhotoVerifierTests.setUpClass()
        cls.index, cls.stages = GroundPhotoVerifierTests.index, GroundPhotoVerifierTests.stages
        cls.fixture = json.loads((ROOT / 'tests/fixtures/ground_cached_card.json').read_bytes())

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='ground-cache-verifier-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        shutil.copytree(ROOT / 'tests/fixtures/ground_cache_preview_bundle', self.root, dirs_exist_ok=True)
        self.photo, self.files = deepcopy(self.fixture['photo']), deepcopy(self.fixture['files'])
        self.ident = self.fixture['day_id']

    def inspect(self):
        return V.verify_photo(self.root, self.photo, self.ident, self.stages[self.ident], self.index, V.PublicSourceReader(self.root), self.files)

    def change_metadata(self, change):
        path = self.root / self.photo['source_metadata_path']
        metadata = json.loads(path.read_bytes())
        change(metadata)
        raw = (json.dumps(metadata, indent=2) + '\n').encode()
        path.write_bytes(raw)
        next(iter(self.files.values()))['metadata_sha256'] = V.sha(raw)

    def assert_failure(self, name, result):
        self.assertFalse(result['passed'])
        self.assertTrue(any(name in message for message in result['failures']), result['failures'])

    def test_real_licensed_cached_ground_photo_decodes(self):
        result = self.inspect()
        self.assertTrue(result['passed'], result['failures'])
        self.assertIn('decoded_ground_dimensions', result['checks'])
        self.assertTrue(result['local_cache_required'])

    def test_remote_only_ground_card_cannot_count_toward_offline_minimum(self):
        self.photo['thumbnail_url'] = self.photo['remote_thumbnail_url']
        self.assert_failure('local_ground_asset', self.inspect())

    def test_cached_source_coordinate_change_rejected_after_metadata_reseal(self):
        self.change_metadata(lambda m: m.update(latitude=m['latitude'] + .001))
        self.assert_failure('ground_cached_provenance_identity', self.inspect())

    def test_resealed_corrupt_cached_ground_bytes_still_fail_decoding(self):
        relative, record = next(iter(self.files.items()))
        path = self.root / relative
        raw = bytearray(path.read_bytes())
        raw[0] = 0
        path.write_bytes(raw)
        digest = V.sha(raw)
        self.photo['image_sha256'] = record['sha256'] = digest
        self.change_metadata(lambda m: m.update(image_sha256=digest))
        self.assert_failure('photo verification could not complete', self.inspect())


class AerialTileVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not hasattr(GroundPhotoVerifierTests, 'index'):
            GroundPhotoVerifierTests.setUpClass()
        cls.index, cls.stages = GroundPhotoVerifierTests.index, GroundPhotoVerifierTests.stages
        cls.fixture = json.loads((ROOT / 'tests/fixtures/aerial_tile_card.json').read_text(encoding='utf-8'))

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='aerial-tile-verifier-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / 'tests/fixtures/aerial_preview_bundle', self.root, dirs_exist_ok=True)
        self.photo, self.files = deepcopy(self.fixture['photo']), deepcopy(self.fixture['files'])
        self.ident = self.fixture['day_id']

    def inspect(self):
        return V.verify_photo(self.root, self.photo, self.ident, self.stages[self.ident], self.index, V.PublicSourceReader(self.root), self.files)

    def change_metadata(self, change):
        path = self.root / self.photo['source_metadata_path']
        metadata = json.loads(path.read_text(encoding='utf-8'))
        change(metadata)
        raw = (json.dumps(metadata, indent=2) + '\n').encode()
        path.write_bytes(raw)
        next(iter(self.files.values()))['metadata_sha256'] = V.sha(raw)

    def assert_failure(self, name, result):
        self.assertFalse(result['passed'])
        self.assertTrue(any(name in f for f in result['failures']), result['failures'])

    def test_real_uncropped_tile_geographic_registration(self):
        result = self.inspect()
        self.assertTrue(result['passed'], result['failures'])
        self.assertIn('aerial_tile_matrix_bounds', result['checks'])
        self.assertIn('aerial_trail_witness_inside_tile', result['checks'])

    def test_resealed_native_extent_cannot_move_tile(self):
        self.change_metadata(lambda m: m['tile']['native_extent'].update(xmin=m['tile']['native_extent']['xmin'] + 100))
        self.assert_failure('aerial_tile_matrix_bounds', self.inspect())

    def test_resealed_center_cannot_move_actual_center_pixel(self):
        self.photo['longitude'] += .001
        self.change_metadata(lambda m: m.update(center_longitude=self.photo['longitude']))
        self.assert_failure('aerial_tile_pixel_center', self.inspect())

    def test_resealed_witness_outside_tile_is_rejected(self):
        witness = deepcopy(self.photo['assignment']['route_witness'])
        witness['latitude'] += .1
        self.photo['assignment']['route_witness'] = witness
        self.change_metadata(lambda m: m.update(route_witness=witness))
        self.assert_failure('aerial_trail_witness_inside_tile', self.inspect())

    def test_false_zero_offset_claim_is_rejected(self):
        self.photo['assignment']['distance_meters'] = 0
        self.photo['distance_to_section_meters'] = 0
        self.assert_failure('aerial_tile_measured_offset', self.inspect())

    def test_resealed_request_for_other_tile_is_rejected(self):
        self.photo['source_url'] += '0'
        self.change_metadata(lambda m: m.update(request_url=self.photo['source_url']))
        self.assert_failure('aerial_official_tile_request', self.inspect())

    def test_resealed_corrupt_raster_still_fails_decoding(self):
        relative, record = next(iter(self.files.items()))
        path = self.root / relative
        raw = bytearray(path.read_bytes())
        raw[0] = 0
        path.write_bytes(raw)
        digest = V.sha(raw)
        self.photo['image_sha256'] = record['sha256'] = digest
        self.change_metadata(lambda m: m.update(image_sha256=digest))
        self.assert_failure('photo verification could not complete', self.inspect())


if __name__ == '__main__':
    unittest.main(verbosity=2)
