"""Dependency-free source/package checks. Does not run MATLAB or install Skills."""
from pathlib import Path
import argparse,hashlib,json,re,zipfile,sys
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def all_files(root):
 return sorted(p for p in root.rglob('*') if p.is_file() and not any(x in {'.git','dist','build','.test-runs','__pycache__'} for x in p.relative_to(root).parts))
def inspect_source(check_manifest=True):
 required=['README.md','README.zh-CN.md','LICENSE','NOTICE','SKILL.md','agents/openai.yaml','references/engineering.md','references/verification.md','references/local-toolchain.md','references/runtime-diagnostics.md','manifests/dependencies.json','manifests/candidate-baseline.json','installer/install.ps1','installer/verify.ps1','installer/rollback.ps1','installer/common.ps1','.github/workflows/release-checks.yml']
 for n in required:assert (ROOT/n).is_file(),f'MISSING: {n}'
 base=json.loads((ROOT/'manifests/candidate-baseline.json').read_text('utf-8'))
 assert base['version']=='2.5.1-rc1' and len(base['main_files'])==6
 for f in base['main_files']:assert digest(ROOT/f['relative'])==f['sha256'],f"CANDIDATE_CHANGED: {f['relative']}"
 body=(ROOT/'SKILL.md').read_text('utf-8-sig');assert body.startswith('---\n') or body.startswith('---\r\n')
 assert re.search(r'^name: aircraft-control-modeling\s*$',body,re.M) and 'description:' in body
 for ref in set(re.findall(r'references/[A-Za-z0-9_-]+\.md',body)):assert (ROOT/ref).is_file(),ref
 deps=json.loads((ROOT/'manifests/dependencies.json').read_text('utf-8'));required_count=0;bundled=0
 for d in deps['dependencies']:
  assert d['kind'] in {'required','conditional','optional'}
  if d['required']:required_count+=1;assert d.get('bundled'),f"UNRESOLVED_REQUIRED: {d['name']}"
  if not d.get('bundled'):assert d.get('status')=='UNVERIFIED';continue
  bundled+=1
  assert re.fullmatch('[a-f0-9]{40}',d['commit']) and d['repository']=='https://github.com/matlab/simulink-agentic-toolkit'
  assert '/'+d['commit']+'/' in d['official_source'] and d['license_file']
  assert (ROOT/'third-party'/d['license_file']).is_file()
  folder=ROOT/'third-party/skills'/d['name'];expected={f['relative']:f['sha256'] for f in d['files']}
  actual={p.relative_to(folder).as_posix():digest(p) for p in folder.rglob('*') if p.is_file()};assert actual==expected,d['name']
 assert required_count==2 and bundled==11
 assert 'Apache License' in (ROOT/'LICENSE').read_text('utf-8') and 'Tide827' in (ROOT/'NOTICE').read_text('utf-8')
 for p in all_files(ROOT):
  if p.suffix not in {'.md','.json','.py','.ps1','.bat','.yml','.yaml','.m'} and p.name not in {'LICENSE','NOTICE','.gitignore','.gitattributes','SHA256SUMS.txt'}:raise AssertionError(f'UNREVIEWED_FILE_TYPE: {p.name}')
  text=p.read_text('utf-8-sig')
  # Source patterns are general; never embed personal host names in this checker.
  assert not re.search(r'[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9_.-]+',text),f'PERSONAL_PATH: {p.relative_to(ROOT)}'
  assert not re.search(r'(?:ghp_|github_pat_|sk-)[A-Za-z0-9_]{25,}|-----BEGIN [A-Z ]*PRIVATE KEY',text),f'SECRET: {p.relative_to(ROOT)}'
  assert not re.search(r'[\w.+-]+@(?:gmail|qq|outlook|hotmail)\.',text,re.I),f'PERSONAL_EMAIL: {p.relative_to(ROOT)}'
  if p.suffix=='.md':
   for u in re.findall(r'\]\(([^)]+)\)',text):
    if re.match(r'[a-zA-Z]+:|#',u) or any(c in u for c in '<>{} '):continue
    local=u.split('#')[0];assert (p.parent/local).exists(),f'BROKEN_LINK {p.relative_to(ROOT)} -> {u}'
   if p.relative_to(ROOT).parts[0]!='third-party':
    assert not any(line.rstrip(' \t')!=line for line in text.splitlines()),f'TRAILING_WHITESPACE: {p.relative_to(ROOT)}'
 if check_manifest:
  mf=json.loads((ROOT/'manifests/release-manifest.json').read_text('utf-8'))
  actual={p.relative_to(ROOT).as_posix():digest(p) for p in all_files(ROOT) if p.relative_to(ROOT).as_posix() not in {'manifests/release-manifest.json','SHA256SUMS.txt'}}
  assert actual=={f['path']:f['sha256'] for f in mf['files']},'RELEASE_MANIFEST_MISMATCH'
  sums=(ROOT/'SHA256SUMS.txt').read_text('utf-8').splitlines()
  assert len(sums)==len(actual)+1
  for line in sums:
   h,n=line.split('  ',1);assert digest(ROOT/n)==h,n
 return {'required_skills':required_count,'bundled_skills':bundled,'source_files':len(all_files(ROOT)),'main_files':6,'status':'PASS'}
def inspect_zip(path):
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None
  names=z.namelist();assert len(names)==len(set(names));prefix='Aircraft-Control-Modeling-v2.5.1-rc1-Installer/'
  assert all(n.startswith(prefix) and '..' not in n.split('/') and not n.startswith('/') for n in names)
  payload={n[len(prefix):]:z.read(n) for n in names}
  mf=json.loads(payload['manifest.json']);expected={f['relative']:f['sha256'] for f in mf['files']}
  actual={n:hashlib.sha256(v).hexdigest() for n,v in payload.items() if n not in {'manifest.json','reports/file_manifest.sha256'}}
  assert actual==expected
  for line in payload['reports/file_manifest.sha256'].decode('utf-8').splitlines():
   h,n=line.split('  ',1);assert hashlib.sha256(payload[n]).hexdigest()==h
  base=json.loads((ROOT/'manifests/candidate-baseline.json').read_text('utf-8'))
  for f in base['main_files']:assert hashlib.sha256(payload['payload/aircraft-control-modeling/'+f['relative']]).hexdigest()==f['sha256']
  assert {'install.bat','安装.bat','LICENSE','NOTICE','dependencies.json'}.issubset(payload)
  for n,data in payload.items():
   text=data.decode('utf-8-sig');assert not re.search(r'[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9_.-]+|(?:ghp_|github_pat_|sk-)[A-Za-z0-9_]{25,}',text),n
 return {'status':'PASS','files':len(payload),'bytes':path.stat().st_size,'sha256':digest(path)}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--zip',type=Path);ap.add_argument('--no-manifest',action='store_true');a=ap.parse_args()
 try:print(json.dumps({'source':inspect_source(not a.no_manifest),'archive':inspect_zip(a.zip) if a.zip else 'not requested'},ensure_ascii=False,indent=2))
 except Exception as e:print('CHECK_FAIL:',str(e),file=sys.stderr);sys.exit(1)
