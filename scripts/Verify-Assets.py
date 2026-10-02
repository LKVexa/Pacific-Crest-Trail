"""Verify published local route assets without modifying hike history."""
import argparse,hashlib,json
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args();root=args.root.resolve()
manifest=json.loads((root/'content'/'asset_manifest.json').read_text(encoding='utf-8'));failures=[]
for name,record in manifest['files'].items():
    path=(root/name).resolve()
    if root not in path.parents or not path.is_file():failures.append(name+': unavailable or outside repository');continue
    if path.stat().st_size!=record['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest()!=record['sha256']:failures.append(name+': checksum or size mismatch')
print(json.dumps({'passed':not failures,'checked':len(manifest['files']),'failures':failures},indent=2));raise SystemExit(1 if failures else 0)
