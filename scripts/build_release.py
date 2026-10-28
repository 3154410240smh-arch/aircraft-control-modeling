"""Build the offline recipient ZIP from reviewed source. Maintainers only; stdlib."""
from pathlib import Path
import hashlib,json,shutil,zipfile,sys
from check_release import ROOT,inspect_source,inspect_zip,digest
NAME='Aircraft-Control-Modeling-v2.5.1-rc1-Installer'
def inventory(root):return [dict(relative=p.relative_to(root).as_posix(),sha256=digest(p),bytes=p.stat().st_size)for p in sorted(root.rglob('*'))if p.is_file()]
def build():
 inspect_source()
 b=ROOT/'build'/NAME
 if b.exists():raise RuntimeError('Build output exists. Use a fresh checkout or archive the old build explicitly; no hidden cleanup.')
 b.mkdir(parents=True);dist=ROOT/'dist';dist.mkdir(exist_ok=True)
 def cp(src,n):
  target=b/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/src,target)
 baseline=json.loads((ROOT/'manifests/candidate-baseline.json').read_text('utf-8'))
 for f in baseline['main_files']:cp(f['relative'],'payload/aircraft-control-modeling/'+f['relative'])
 deps=json.loads((ROOT/'manifests/dependencies.json').read_text('utf-8'))
 for d in deps['dependencies']:
  if d.get('bundled'):
   for f in d['files']:cp('third-party/skills/'+d['name']+'/'+f['relative'],'payload/'+d['name']+'/'+f['relative'])
 for p in (ROOT/'third-party/licenses').iterdir():cp(p.relative_to(ROOT),'licenses/'+p.name)
 for p in (ROOT/'installer').iterdir():cp(p.relative_to(ROOT),'installer/'+p.name)
 for n in ['install.bat','安装.bat','verify.bat','rollback.bat','LICENSE','NOTICE']:cp(n,n)
 cp('manifests/dependencies.json','dependencies.json');cp('manifests/dependency-audit.json','reports/dependency_audit.json')
 cp('tests/fixtures/prior-installation-summary.json','reports/prior-installation-summary.json')
 cp('docs/installation.md','README_安装说明.md')
 (b/'依赖清单.md').write_text('# 依赖清单\n\n见 [dependencies.json](dependencies.json) 的完整名称、版本、commit、文件 SHA 和许可路径；官方原许可在 licenses/，详细规则见 [依赖政策](docs/dependency-policy.md)。包含2个必需和9个条件辅助 Skill，另6个条件路由未打包。MATLAB/Simulink/SATK/MCP是独立外部工具链，不会自动安装。\n',encoding='utf-8')
 # Root README is self-contained; repository-relative docs are supplied as extra reference material.
 readme='''# Windows one-click installer / 一键安装

Verify the ZIP SHA-256 from the GitHub pre-release, fully extract, then double-click install.bat (安装.bat). Run verify.bat after installation. Windows PowerShell 5.1+, no Python/Git/admin. Default offline main+2 required+9 verified conditional auxiliary Skills. Existing identical files are reused; auxiliary conflicts stop; main upgrades require explicit YES and a complete backup. Six unbundled specialist routes remain conditional. External MATLAB/Simulink/SATK/MCP are NOT installed or configured.

检查压缩包哈希后完整解压，双击 install.bat（或安装.bat）；verify.bat 检查文件。保留安装时打印的 receipt 路径。需要回滚时运行 rollback.bat 并粘贴该路径；仅撤销本事务修改，不删除此前复用的依赖，后续用户改动会阻止覆盖。不要关闭安全策略或使用管理员权限。

Logs, staging, backups and quarantine are outside skills under CODEX_HOME/.acm-installer/transaction. Read logs before repeating a failed install. Matching content defines compatibility; no implicit dependency upgrades. Restart/new-session Codex using supported UI and verify the discovered Skill path. Disk files do not prove desktop activation or toolchain availability.

Official Skill licenses are retained in licenses/. Project-authored files: Apache-2.0, Copyright 2026 Tide827. Auxiliary MathWorks materials remain under their separate restricted-use licenses, NOT Apache-2.0; see NOTICE and dependencies.json. No geometry executor, runtime Grant, MATLAB binary or license is included.

Documentation and issue tracker: https://github.com/3154410240smh-arch/aircraft-control-modeling . Pre-release v2.5.1-rc1 is not a stable universal layout or flight-control product. Obtain new releases explicitly; do not use GitHub's generic source archive as the installer.
'''
 (b/'README_接收者使用说明.md').write_text(readme,encoding='utf-8')
 # Detailed docs retain their relative-link validity in their own directory tree.
 for p in (ROOT/'docs').glob('*.md'):cp(p.relative_to(ROOT),'docs/'+p.name)
 for n in ['SECURITY.md','CONTRIBUTING.md','CODE_OF_CONDUCT.md']:cp(n,n)
 cp('manifests/dependencies.json','manifests/dependencies.json')
 skills=[]
 for p in sorted((b/'payload').iterdir()):
  dep=next((d for d in deps['dependencies']if d['name']==p.name),None)
  skills.append(dict(name=p.name,kind=dep['kind']if dep else 'main',version=dep['version']if dep else '2.5.1-rc1',payload='payload/'+p.name,files=inventory(p)))
 mf=dict(format_version=1,version='2.5.1-rc1',skills=skills,files=inventory(b))
 (b/'manifest.json').write_text(json.dumps(mf,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (b/'reports/file_manifest.sha256').write_text(''.join(f"{f['sha256']}  {f['relative']}\n"for f in inventory(b)),encoding='utf-8')
 zpath=dist/(NAME+'.zip')
 if zpath.exists():raise RuntimeError('Frozen ZIP already exists; no silent overwrite')
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(b.rglob('*')):
   if p.is_file():
    info=zipfile.ZipInfo(NAME+'/'+p.relative_to(b).as_posix(),date_time=(2026,10,28,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,p.read_bytes())
 audit=inspect_zip(zpath)
 for src,dest in [('manifests/release-manifest.json','release-manifest.json'),('release-audit.md','release-audit.md'),('tests/INSTALLATION_TEST_REPORT.md','INSTALLATION_TEST_REPORT.md'),('docs/dependency-policy.md','DEPENDENCY_AUDIT.md'),('README.zh-CN.md','README_发布与使用说明.md')]:shutil.copyfile(ROOT/src,dist/dest)
 (dist/'SHA256SUMS.txt').write_text(''.join(f'{digest(p)}  {p.name}\n'for p in sorted(dist.iterdir())if p.is_file() and p.name!='SHA256SUMS.txt'),encoding='utf-8')
 print(json.dumps(audit,ensure_ascii=False,indent=2));return zpath
if __name__=='__main__':build()
