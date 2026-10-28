"""Explicit reviewed release freeze; does not change candidate Skill files."""
from pathlib import Path
import json
from check_release import ROOT,all_files,digest,inspect_source
if __name__=='__main__':
 inspect_source(False)
 files=[dict(path=p.relative_to(ROOT).as_posix(),sha256=digest(p),bytes=p.stat().st_size,origin=('accepted frozen main Skill' if p.relative_to(ROOT).as_posix()in{f['relative']for f in json.loads((ROOT/'manifests/candidate-baseline.json').read_text('utf-8'))['main_files']}else 'MathWorks pinned dependency' if p.relative_to(ROOT).parts[0]=='third-party'else 'Tide827 project publication'),license=('see retained MathWorks license'if p.relative_to(ROOT).parts[0]=='third-party'else 'Apache-2.0'))for p in all_files(ROOT)if p.relative_to(ROOT).as_posix()not in{'manifests/release-manifest.json','SHA256SUMS.txt'}]
 mf=dict(schema_version=1,version='2.5.1-rc1',release_type='pre-release',copyright='2026 Tide827',files=files,evidence='examples/quadrotor-lqi/README.md',candidate_baseline='manifests/candidate-baseline.json',artifact={'name':'Aircraft-Control-Modeling-v2.5.1-rc1-Installer.zip','sha256_file':'SHA256SUMS.txt in release assets','contents_manifest':'manifest.json inside installer archive'})
 (ROOT/'manifests/release-manifest.json').write_text(json.dumps(mf,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (ROOT/'SHA256SUMS.txt').write_text(''.join(f'{digest(p)}  {p.relative_to(ROOT).as_posix()}\n'for p in all_files(ROOT)if p.name!='SHA256SUMS.txt'),encoding='utf-8')
 print(json.dumps(inspect_source(),indent=2))
