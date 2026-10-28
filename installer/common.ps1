Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
function Hash([string]$p) {
 $s=[IO.File]::OpenRead($p);$a=[Security.Cryptography.SHA256]::Create()
 try{return ([BitConverter]::ToString($a.ComputeHash($s))).Replace('-','').ToLowerInvariant()}finally{$s.Dispose();$a.Dispose()}
}
function Full([string]$p) { [IO.Path]::GetFullPath($p).TrimEnd('\') }
function Safe([string]$p) {
 $q=Full $p
 if($q.IndexOf(':',2) -ge 0){throw "Unsafe path: $p"}
 $a=$q
 while($a){
  if(Test-Path -LiteralPath $a){if(([IO.File]::GetAttributes($a) -band [IO.FileAttributes]::ReparsePoint) -ne 0){throw "Reparse point rejected: $a"}}
  $a=[IO.Path]::GetDirectoryName($a)
 }
 return $q
}
function Under([string]$parent,[string]$child) {
 $p=Safe $parent; $c=Safe $child
 if(-not $c.StartsWith($p+'\',[StringComparison]::OrdinalIgnoreCase)){throw "Path escapes root: $c"};return $c
}
function Files([string]$dir) {
 $root=Safe $dir
 if(-not (Test-Path -LiteralPath $root -PathType Container)){throw "Missing directory: $root"}
 $out=@()
 foreach($f in @(Get-ChildItem -LiteralPath $root -Recurse -Force -File)){
  $null=Safe $f.FullName
  $out+= [pscustomobject]@{relative=$f.FullName.Substring($root.Length+1).Replace('\','/');sha256=(Hash $f.FullName);bytes=$f.Length}
 }
 # Also reject empty junctions, which a file-only inventory would miss.
 foreach($d in @(Get-ChildItem -LiteralPath $root -Recurse -Force -Directory)){$null=Safe $d.FullName}
 return @($out | Sort-Object relative)
}
function Match([string]$dir,$expected) {
 if(-not(Test-Path -LiteralPath $dir -PathType Container)){return $false}
 $actual=@(Files $dir);$exp=@($expected)
 if($actual.Count -ne $exp.Count){return $false}
 foreach($e in $exp){$a=@($actual|Where-Object {$_.relative -ceq $e.relative});if($a.Count -ne 1 -or $a[0].sha256 -cne $e.sha256){return $false}}
 return $true
}
function WriteJson($path,$obj){
 $s=$obj|ConvertTo-Json -Depth 40;[IO.File]::WriteAllText($path,$s,(New-Object Text.UTF8Encoding($true)))
 if([IO.Path]::GetFileName($path) -ceq 'receipt.json'){
  $event=[pscustomobject]@{time=(Get-Date).ToString('o');receipt=$obj}|ConvertTo-Json -Depth 42 -Compress
  [IO.File]::AppendAllText((Join-Path (Split-Path $path -Parent) 'events.jsonl'),$event+[Environment]::NewLine,(New-Object Text.UTF8Encoding($false)))
 }
}
function LoadPackage {
 $script:Package=Safe (Split-Path $PSScriptRoot -Parent)
 if(-not(Test-Path -LiteralPath (Join-Path $Package 'manifest.json'))){throw 'SOURCE_CHECKOUT: use the named Release Installer ZIP or build scripts/build_release.py first'}
 $script:Manifest=Get-Content -LiteralPath (Join-Path $Package 'manifest.json') -Raw -Encoding UTF8|ConvertFrom-Json
 $expected=@($Manifest.files);$actual=@(Files $Package|Where-Object {$_.relative -notin @('manifest.json','reports/file_manifest.sha256')})
 if($actual.Count -ne $expected.Count){throw 'PACKAGE_FAIL: unexpected file set'}
 foreach($e in $expected){
  $p=Under $Package (Join-Path $Package $e.relative)
  if(-not(Test-Path -LiteralPath $p -PathType Leaf) -or (Hash $p) -cne $e.sha256){throw "PACKAGE_FAIL: $($e.relative)"}
 }
 foreach($a in $actual){if(@($expected|Where-Object {$_.relative -ceq $a.relative}).Count -ne 1){throw 'PACKAGE_FAIL: unexpected path'}}
 # Verify the manifest too, against the external-to-manifest digest list.
 $lines=Get-Content -LiteralPath (Join-Path $Package 'reports/file_manifest.sha256') -Encoding UTF8
 if(@($lines).Count -ne ($expected.Count+1)){throw 'PACKAGE_FAIL: digest list count'}
 foreach($l in $lines){if($l -notmatch '^([a-f0-9]{64})  (.+)$'){throw 'PACKAGE_FAIL: malformed digest'};$p=Under $Package (Join-Path $Package $Matches[2]);if((Hash $p) -cne $Matches[1]){throw "PACKAGE_FAIL: digest $p"}}
}
function Context([string]$TestRoot) {
 if($TestRoot){
  $r=Safe $TestRoot
  $m=Join-Path $r '.acm-install-test.json'
  if(-not(Test-Path -LiteralPath $m)){throw 'TestRoot marker required'}
  $j=Get-Content -LiteralPath $m -Raw|ConvertFrom-Json
  if($j.purpose -cne 'isolated-acm-installer-test'){throw 'Invalid test marker'}
  $script:InstallHome=Under $r (Join-Path $r 'codex');$script:Agents=Under $r (Join-Path $r 'agents')
 }else{
  if($env:CODEX_HOME){$script:InstallHome=Safe $env:CODEX_HOME}else{$script:InstallHome=Safe (Join-Path $env:USERPROFILE '.codex')}
  $script:Agents=Safe (Join-Path $env:USERPROFILE '.agents\skills')
 }
 $script:Skills=Under $InstallHome (Join-Path $InstallHome 'skills')
 $script:Records=Under $InstallHome (Join-Path $InstallHome '.acm-installer')
}
function CopyTree([string]$from,[string]$to) {
 $null=Safe $from;$null=Safe $to
 if(Test-Path -LiteralPath $to){throw "Destination already exists: $to"}
 $null=New-Item -ItemType Directory -Path $to
 foreach($f in @(Files $from)){
  $dest=Under $to (Join-Path $to $f.relative);$null=New-Item -ItemType Directory -Force -Path (Split-Path $dest -Parent)
  [IO.File]::Copy((Join-Path $from $f.relative),$dest,$false)
 }
}
function Undo($receipt,[string]$tx) {
 # Preflight every object before reverting any object; never discard user edits.
 foreach($c in @($receipt.changes)){
  $dest=Under $Skills $c.destination
  if(Test-Path -LiteralPath $dest){if(-not(Match $dest $c.after)){throw "ROLLBACK_BLOCKED: modified after installation: $dest"}}
  if($c.backup -and (Test-Path -LiteralPath $c.backup)){if(-not(Match $c.backup $c.before)){throw 'ROLLBACK_BLOCKED: backup mismatch'}}
 }
 $items=@($receipt.changes);[array]::Reverse($items)
 foreach($c in $items){
  $dest=Under $Skills $c.destination
  if(Test-Path -LiteralPath $dest){$q=Under $tx (Join-Path $tx ('quarantine-'+$c.name));[IO.Directory]::Move($dest,$q)}
  if($c.backup -and (Test-Path -LiteralPath $c.backup)){[IO.Directory]::Move($c.backup,$dest);if(-not(Match $dest $c.before)){throw 'ROLLBACK_FAIL: restored hash'}}
  $c.state='reverted'
 }
 $receipt.status='ROLLED_BACK';WriteJson (Join-Path $tx 'receipt.json') $receipt
}
