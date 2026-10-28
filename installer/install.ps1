#requires -Version 5.1
[CmdletBinding()]
param([string]$TestRoot='', [switch]$Interactive,[switch]$ApproveMainReplacement,
 [ValidateSet('Offline','Online')][string]$SourceMode='Offline', [string]$TestProxy='', [int]$TestFailAfterWrites=0)
. "$PSScriptRoot\common.ps1"
$lock=$null;$tx=$null;$receipt=$null
try {
 if([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT){throw 'Windows required'}
 LoadPackage;Context $TestRoot
 if(($TestProxy -or $TestFailAfterWrites) -and -not $TestRoot){throw 'Fault injection restricted to marked sandbox'}
 $null=New-Item -ItemType Directory -Force -Path $Skills
 $null=New-Item -ItemType Directory -Force -Path $Records
 $lock=[IO.File]::Open((Join-Path $Records 'writer.lock'),'OpenOrCreate','ReadWrite','None')
 # Actual write-access test; does not alter any Skill. Keep a small audit probe.
 $probe=Under $Skills (Join-Path $Skills ('.acm-write-probe-'+[guid]::NewGuid().ToString('N')))
 [IO.File]::WriteAllText($probe,'installer write-access probe')
 [IO.File]::Move($probe,(Join-Path $Records ([IO.Path]::GetFileName($probe))))
 $tx=Under $Records (Join-Path $Records ((Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[guid]::NewGuid().ToString('N')))
 $null=New-Item -ItemType Directory -Path $tx
 $receipt=[pscustomobject]@{version=$Manifest.version;status='PREPARING';time=(Get-Date).ToString('o');package_manifest=(Hash (Join-Path $Package 'manifest.json'));skills_root=$Skills;changes=@();reused=@();error='';rollback_error=''}
 WriteJson (Join-Path $tx 'receipt.json') $receipt
 $plan=@()
 foreach($s in @($Manifest.skills)){
  $dest=Under $Skills (Join-Path $Skills $s.name)
  $locations=@($dest)
  if($s.kind -ne 'main'){$locations+= (Under $Agents (Join-Path $Agents $s.name))}
  $existing=@($locations|Select-Object -Unique|Where-Object {Test-Path -LiteralPath $_})
  $replace=$false
  foreach($p in $existing){
   if(-not(Match $p $s.files)){
    if($s.kind -eq 'main' -and $p -eq $dest){
     Write-Host "MAIN_CONFLICT: $p. Existing content differs; complete backup required."
     $actual=@(Files $p)
     foreach($f in @($s.files)){$old=@($actual|Where-Object {$_.relative -ceq $f.relative});$oldHash='MISSING';if($old.Count -eq 1){$oldHash=$old[0].sha256};if($oldHash -cne $f.sha256){Write-Host "DIFF $($f.relative): installed=$oldHash candidate=$($f.sha256)"}}
     foreach($f in $actual){if(@($s.files|Where-Object {$_.relative -ceq $f.relative}).Count -eq 0){Write-Host "EXTRA_INSTALLED_FILE: $($f.relative) SHA256=$($f.sha256)"}}
     if(-not $ApproveMainReplacement){if($Interactive){$answer=Read-Host 'Replace the main Skill after full backup? Type YES';if($answer -ceq 'YES'){$ApproveMainReplacement=$true}}}
     if(-not $ApproveMainReplacement){throw 'MAIN_CONFLICT: explicit approval required'}
     $replace=$true
    }else{throw "DEPENDENCY_CONFLICT: $($s.name) at $p; no dependency upgrade/downgrade performed"}
   }
  }
  if($existing.Count -gt 0 -and -not $replace){$receipt.reused+= [pscustomobject]@{name=$s.name;paths=$existing;files=$s.files};continue}
  $plan+= [pscustomobject]@{skill=$s;destination=$dest;replace=$replace}
 }
 WriteJson (Join-Path $tx 'receipt.json') $receipt
 $need=0L
 foreach($p in $plan){foreach($f in @($p.skill.files)){$need+=[long]$f.bytes};if($p.replace){foreach($f in @(Files $p.destination)){$need+=[long]$f.bytes}}}
 $drive=New-Object IO.DriveInfo ([IO.Path]::GetPathRoot($InstallHome))
 if($drive.AvailableFreeSpace -lt ($need*2+10485760)){throw 'INSUFFICIENT_DISK_SPACE'}
 # All payload staged and verified before the first Skill write.
 foreach($p in $plan){
  $s=$p.skill;$stage=Under $tx (Join-Path $tx ('stage-'+$s.name))
  if($SourceMode -eq 'Online' -and $s.kind -ne 'main'){
   $dep=@((Get-Content -LiteralPath (Join-Path $Package 'dependencies.json') -Raw -Encoding UTF8|ConvertFrom-Json).dependencies|Where-Object {$_.name -ceq $s.name -and $_.bundled})[0]
   $null=New-Item -ItemType Directory -Path $stage
   foreach($f in @($s.files)){
    $target=Under $stage (Join-Path $stage $f.relative);$null=New-Item -ItemType Directory -Force -Path (Split-Path $target -Parent)
    $args=@{Uri=($dep.raw_base+$f.relative);OutFile=$target;UseBasicParsing=$true;TimeoutSec=20;ErrorAction='Stop'}
    if($TestProxy){$args.Proxy=$TestProxy}
    Invoke-WebRequest @args
   }
  }else{CopyTree (Join-Path $Package $s.payload) $stage}
  if(-not(Match $stage $s.files)){throw "STAGING_HASH_FAIL: $($s.name)"}
 }
 $receipt.status='INSTALLING';WriteJson (Join-Path $tx 'receipt.json') $receipt
 $writes=0
 foreach($p in $plan){
  $s=$p.skill;$backup='';$before=@()
  if($p.replace){$before=@(Files $p.destination);$backup=Under $tx (Join-Path $tx ('backup-'+$s.name))}
  $change=[pscustomobject]@{name=$s.name;destination=$p.destination;backup=$backup;before=$before;after=@($s.files);state='planned'}
  $receipt.changes+= $change;WriteJson (Join-Path $tx 'receipt.json') $receipt
  if($p.replace){[IO.Directory]::Move($p.destination,$backup);$change.state='old_moved';WriteJson (Join-Path $tx 'receipt.json') $receipt;if(-not(Match $backup $before)){throw 'BACKUP_HASH_FAIL'}}
  [IO.Directory]::Move((Join-Path $tx ('stage-'+$s.name)),$p.destination)
  $change.state='installed';WriteJson (Join-Path $tx 'receipt.json') $receipt
  if(-not(Match $p.destination $s.files)){throw 'INSTALL_HASH_FAIL'}
  $writes++
  if($TestFailAfterWrites -gt 0 -and $writes -eq $TestFailAfterWrites){throw 'INJECTED_MID_INSTALL_FAILURE'}
 }
 foreach($r in @($receipt.reused)){foreach($p in @($r.paths)){if(-not(Match $p $r.files)){throw 'REUSED_DEPENDENCY_CHANGED'}}}
 $receipt.status='INSTALLED';WriteJson (Join-Path $tx 'receipt.json') $receipt
 Write-Host "INSTALL_PASS: $Skills";Write-Host "Receipt: $(Join-Path $tx 'receipt.json')"
 Write-Host 'MATLAB/SATK/MCP toolchain and current desktop Skill discovery: UNVERIFIED.'
 exit 0
} catch {
 $msg=$_.Exception.Message;Write-Host "INSTALL_FAIL: $msg"
 if(-not $receipt -and (Get-Variable Records -Scope Script -ErrorAction SilentlyContinue) -and (Test-Path -LiteralPath $Records)){
  try{WriteJson (Join-Path $Records ('preflight-failure-'+[guid]::NewGuid().ToString('N')+'.json')) ([pscustomobject]@{status='FAILED_BEFORE_SKILL_WRITES';error=$msg;time=(Get-Date).ToString('o')})}catch{Write-Host 'Unable to write preflight log; preserve console error.'}
 }
 if($receipt){$receipt.error=$msg;WriteJson (Join-Path $tx 'receipt.json') $receipt
  try{if(@($receipt.changes).Count -gt 0){Undo $receipt $tx;Write-Host 'Automatic rollback completed.'}else{$receipt.status='FAILED_BEFORE_SKILL_WRITES';WriteJson (Join-Path $tx 'receipt.json') $receipt}}
  catch{$receipt.status='ROLLBACK_BLOCKED';$receipt.rollback_error=$_.Exception.Message;WriteJson (Join-Path $tx 'receipt.json') $receipt;Write-Host "ROLLBACK_BLOCKED: $($receipt.rollback_error)"}
 }
 exit 1
} finally {if($lock){$lock.Dispose()}}
