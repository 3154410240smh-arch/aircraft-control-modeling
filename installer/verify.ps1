[CmdletBinding()]param([string]$TestRoot='')
. "$PSScriptRoot\common.ps1"
try {
 LoadPackage;Context $TestRoot
 $results=@()
 foreach($s in @($Manifest.skills)){
  $paths=@((Join-Path $Skills $s.name));if($s.kind -ne 'main'){$paths+= (Join-Path $Agents $s.name)}
  $found=@($paths|Select-Object -Unique|Where-Object {Test-Path -LiteralPath $_})
  if($found.Count -eq 0){throw "MISSING_SKILL: $($s.name)"}
  foreach($p in $found){if(-not(Match $p $s.files)){throw "INSTALLED_HASH_CONFLICT: $p"}}
  $results+= [pscustomobject]@{name=$s.name;status='PASS';paths=$found}
 }
 $main=Join-Path $Skills 'aircraft-control-modeling'
 $body=Get-Content -LiteralPath (Join-Path $main 'SKILL.md') -Raw -Encoding UTF8
 foreach($m in [regex]::Matches($body,'references/[A-Za-z0-9_-]+\.md')){if(-not(Test-Path -LiteralPath (Join-Path $main $m.Value))){throw "BROKEN_REFERENCE: $($m.Value)"}}
 $results|ConvertTo-Json -Depth 6|Write-Output
 Write-Host 'FILES_AND_BUNDLED_DEPENDENCIES_PASS. Conditional unbundled routes and external toolchain remain UNVERIFIED.';exit 0
}catch{Write-Host "VERIFY_FAIL: $($_.Exception.Message)";exit 1}
