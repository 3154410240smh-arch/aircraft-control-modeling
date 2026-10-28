[CmdletBinding()]param([string]$Receipt='',[string]$TestRoot='',[switch]$Interactive)
. "$PSScriptRoot\common.ps1"
$lock=$null
try {
 LoadPackage;Context $TestRoot
 if(-not $Receipt -and $Interactive){$Receipt=Read-Host 'Paste the exact receipt.json path (no surrounding quotes)'}
 if(-not $Receipt){throw 'Receipt path required'}
 $rpath=Under $Records $Receipt;$tx=Split-Path $rpath -Parent
 if([IO.Path]::GetFileName($rpath) -cne 'receipt.json'){throw 'Expected installation receipt.json'}
 $r=Get-Content -LiteralPath $rpath -Raw -Encoding UTF8|ConvertFrom-Json
 if($r.skills_root -cne $Skills){throw 'Receipt belongs to another root'}
 if($r.status -notin @('INSTALLED','INSTALLING','ROLLBACK_BLOCKED')){throw "Not rollback eligible: $($r.status)"}
 # A receipt is local audit data, not an arbitrary file-move request.
 foreach($c in @($r.changes)){
  if($c.name -notmatch '^[a-z0-9-]+$' -or $c.destination -cne (Join-Path $Skills $c.name)){throw 'Invalid receipt destination'}
  if($c.backup -and $c.backup -cne (Join-Path $tx ('backup-'+$c.name))){throw 'Invalid receipt backup'}
 }
 $lock=[IO.File]::Open((Join-Path $Records 'writer.lock'),'OpenOrCreate','ReadWrite','None')
 Undo $r $tx;Write-Host 'ROLLBACK_PASS: original Skill state restored; reused dependencies untouched.';exit 0
}catch{Write-Host "ROLLBACK_FAIL: $($_.Exception.Message)";exit 1}
finally{if($lock){$lock.Dispose()}}
