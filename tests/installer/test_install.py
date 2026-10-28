"""Actual isolated Windows installer/failure/rollback tests. No MATLAB calls."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tree(p):return {x.relative_to(p).as_posix():sha(x)for x in p.rglob('*')if x.is_file()}if p.exists()else{}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--zip',type=Path);ap.add_argument('--package',type=Path);a=ap.parse_args()
 if os.name!='nt':raise RuntimeError('Requires actual Windows; do not report native installation PASS on another OS')
 run=ROOT/'.test-runs'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f');run.mkdir(parents=True)
 if a.zip:
  with zipfile.ZipFile(a.zip)as z:
   assert z.testzip()is None
   assert all('..'not in n.split('/')and not n.startswith('/')for n in z.namelist());z.extractall(run/'最终 ZIP 解压')
  package=run/'最终 ZIP 解压'/'Aircraft-Control-Modeling-v2.5.1-rc1-Installer'
 elif a.package:package=a.package.resolve()
 else:raise RuntimeError('--zip or --package required')
 outcomes=[];calls=[]
 def invoke(script,p,*args,b=package):
  cmd=['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(b/'installer'/script),'-TestRoot',str(p),*args]
  start=datetime.datetime.now();o=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
  idx=len(calls)+1;(run/f'call-{idx:02}.txt').write_bytes(o.stdout)
  calls.append({'call':idx,'script':script,'exit':o.returncode,'seconds':(datetime.datetime.now()-start).total_seconds()})
  return o.returncode,o.stdout.decode('utf-8','replace')
 def check(name,ok):
  outcomes.append({'test':name,'status':'PASS'if ok else'FAIL'});print(name,outcomes[-1]['status'],flush=True)
  (run/'results.json').write_text(json.dumps({'tests':outcomes,'calls':calls},ensure_ascii=False,indent=2),encoding='utf-8')
  if not ok:raise AssertionError(name)
 def sb(n):
  p=run/n;p.mkdir();(p/'.acm-install-test.json').write_text('{"purpose":"isolated-acm-installer-test"}');return p
 def receipt(p):return max((p/'codex'/'.acm-installer').glob('*/receipt.json'),key=lambda x:x.stat().st_mtime_ns)
 def add_user(p):
  x=p/'codex'/'skills'/'user-unrelated';x.mkdir(parents=True);(x/'SKILL.md').write_text('user-owned untouched content')
 def cp(name,where):shutil.copytree(package/'payload'/name,where/name)
 p=sb('干净 中文 空格');add_user(p);before=tree(p/'codex'/'skills')
 c,_=invoke('install.ps1',p);check('clean_install',c==0)
 c,_=invoke('verify.ps1',p);check('clean_verify',c==0)
 after=tree(p/'codex'/'skills');c,_=invoke('install.ps1',p);r=json.loads(receipt(p).read_text('utf-8-sig'))
 check('idempotent_reuse',c==0 and not r['changes']and len(r['reused'])==12 and tree(p/'codex'/'skills')==after)
 p=sb('partial');(p/'agents').mkdir();cp('building-simulink-models',p/'agents');cp('simulating-simulink-models',p/'agents');before=tree(p/'agents')
 c,_=invoke('install.ps1',p);check('partial_external_dependency_reuse',c==0 and tree(p/'agents')==before and not(p/'codex'/'skills'/'building-simulink-models').exists())
 c,_=invoke('verify.ps1',p);check('partial_verify',c==0)
 p=sb('dependency-conflict');d=p/'codex'/'skills'/'building-simulink-models';d.mkdir(parents=True);(d/'SKILL.md').write_text('different version');before=tree(p/'codex'/'skills')
 c,o=invoke('install.ps1',p);check('incompatible_dependency_no_write',c!=0 and'DEPENDENCY_CONFLICT'in o and tree(p/'codex'/'skills')==before)
 p=sb('main-conflict');d=p/'codex'/'skills'/'aircraft-control-modeling';d.mkdir(parents=True);(d/'SKILL.md').write_text('original main');(d/'extra.txt').write_text('complete backup');add_user(p);before=tree(p/'codex'/'skills')
 c,o=invoke('install.ps1',p);check('main_conflict_no_silent_overwrite',c!=0 and'MAIN_CONFLICT'in o and tree(p/'codex'/'skills')==before)
 c,_=invoke('install.ps1',p,'-ApproveMainReplacement');rp=receipt(p);r=json.loads(rp.read_text('utf-8-sig'));backup=Path(r['changes'][0]['backup'])
 check('approved_upgrade_complete_backup',c==0 and(backup/'SKILL.md').read_text()=='original main'and(backup/'extra.txt').read_text()=='complete backup')
 c,_=invoke('rollback.ps1',p,'-Receipt',str(rp));check('upgrade_exact_rollback',c==0 and tree(p/'codex'/'skills')==before)
 p=sb('midway');d=p/'codex'/'skills'/'aircraft-control-modeling';d.mkdir(parents=True);(d/'SKILL.md').write_text('preserve main');cp('building-simulink-models',p/'codex'/'skills');add_user(p);before=tree(p/'codex'/'skills')
 c,o=invoke('install.ps1',p,'-ApproveMainReplacement','-TestFailAfterWrites','2');r=json.loads(receipt(p).read_text('utf-8-sig'))
 check('mid_install_auto_rollback',c!=0 and'INJECTED_MID_INSTALL_FAILURE'in o and r['status']=='ROLLED_BACK'and tree(p/'codex'/'skills')==before)
 p=sb('network');add_user(p);before=tree(p/'codex'/'skills');c,_=invoke('install.ps1',p,'-SourceMode','Online','-TestProxy','http://127.0.0.1:9')
 check('actual_network_failure_before_writes',c!=0 and tree(p/'codex'/'skills')==before and not json.loads(receipt(p).read_text('utf-8-sig'))['changes'])
 p=sb('hash');bad=run/'tampered';shutil.copytree(package,bad);(bad/'payload'/'aircraft-control-modeling'/'SKILL.md').write_text('tamper')
 c,o=invoke('install.ps1',p,b=bad);check('hash_failure_before_install',c!=0 and'PACKAGE_FAIL'in o and not(p/'codex').exists())
 p=sb('uninstall');add_user(p);before=tree(p/'codex'/'skills');c,_=invoke('install.ps1',p);rp=receipt(p);c2,_=invoke('rollback.ps1',p,'-Receipt',str(rp))
 check('fresh_install_uninstall_loop',c==0 and c2==0 and tree(p/'codex'/'skills')==before)
 p=sb('later-edit');c,_=invoke('install.ps1',p);rp=receipt(p);(p/'codex'/'skills'/'aircraft-control-modeling'/'SKILL.md').write_text('user edits');before=tree(p/'codex'/'skills');c2,o=invoke('rollback.ps1',p,'-Receipt',str(rp))
 check('rollback_refuses_later_user_edit',c==0 and c2!=0 and'modified after installation'in o and tree(p/'codex'/'skills')==before)
 p=sb('permission');(p/'codex'/'skills').mkdir(parents=True)
 acl=r'''param([string]$Root,[string]$Installer)
$ErrorActionPreference='Stop'
$dest=Join-Path $Root 'codex\skills'
$acl=[IO.Directory]::GetAccessControl($dest)
$sid=[Security.Principal.WindowsIdentity]::GetCurrent().User
$rule=New-Object Security.AccessControl.FileSystemAccessRule($sid,[Security.AccessControl.FileSystemRights]::Write,[Security.AccessControl.InheritanceFlags]'ContainerInherit, ObjectInherit',[Security.AccessControl.PropagationFlags]::None,[Security.AccessControl.AccessControlType]::Deny)
$acl.AddAccessRule($rule)
try {
 [IO.Directory]::SetAccessControl($dest,$acl)
 & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Installer -TestRoot $Root
 if($LASTEXITCODE -eq 0){throw 'Unexpected success under write denial'}
 if(@([IO.Directory]::GetFileSystemEntries($dest)).Count -ne 0){throw 'Files changed under write denial'}
 Write-Output 'PERMISSION_DENIAL_PASS'
}finally{
 $acl.RemoveAccessRuleSpecific($rule);[IO.Directory]::SetAccessControl($dest,$acl)
 $probe=Join-Path $dest '.acl-restored';[IO.File]::WriteAllText($probe,'restored');[IO.File]::Move($probe,(Join-Path $Root 'acl-restored'))
}
'''
 f=run/'acl-test.ps1';f.write_text(acl,encoding='utf-8-sig')
 o=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(f),'-Root',str(p),'-Installer',str(package/'installer/install.ps1')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(run/'acl-output.txt').write_bytes(o.stdout)
 check('actual_ntfs_write_denial',o.returncode==0 and b'PERMISSION_DENIAL_PASS'in o.stdout)
 p=run/'default-path-bat';p.mkdir();(p/'profile').mkdir();env=os.environ.copy();env['CODEX_HOME']=str(p/'codex');env['USERPROFILE']=str(p/'profile')
 for bat in ['install.bat','verify.bat']:
  o=subprocess.run(['cmd.exe','/d','/c',bat],cwd=package,env=env,input=b'\r\n',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90);(run/(bat+'.txt')).write_bytes(o.stdout);check('actual_'+bat,o.returncode==0)
 rp=receipt(p);o=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(package/'installer/rollback.ps1'),'-Receipt',str(rp)],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(run/'bat-rollback.txt').write_bytes(o.stdout)
 check('default_path_rollback',o.returncode==0 and not list((p/'codex'/'skills').glob('*/SKILL.md')))
 print(json.dumps({'status':'PASS','tests':len(outcomes),'evidence':str(run),'toolchain':'UNVERIFIED','desktop_activation':'UNVERIFIED'},ensure_ascii=False))
if __name__=='__main__':main()
