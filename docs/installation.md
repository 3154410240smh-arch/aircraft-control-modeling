# Installation / 安装

## Release ZIP

Download the named Installer.zip asset and SHA256SUMS.txt from the v2.5.1-rc1 pre-release, not GitHub's generic source archive. Verify with `certutil -hashfile <zip> SHA256`; fully extract, then run install.bat. Windows PowerShell 5.1+ is required; no Python/Git/admin is needed by recipients. Spaces/Chinese paths were locally tested.

The package uses CODEX_HOME/skills if CODEX_HOME is already set; otherwise USERPROFILE/.codex/skills. It does not change either variable. Auxiliary versions in USERPROFILE/.agents/skills are also checked for exact reuse/conflict. Plugin/custom discovery paths are not automatically modified or purged. Third-party source and license notices are bundled.

## Verification and discovery

Run verify.bat, retain the printed receipt path, and inspect the explicit result. Installed files are re-read, exact file sets/SHA checked, and main reference paths checked. Start a new Codex session or use its supported restart UI. Ask it to list/resolve `$aircraft-control-modeling` and confirm the actual installation path/version. If an old session remains cached, do not infer activation from files on disk. The release records only an independent Codex product metadata scan; recipient desktop activation remains UNVERIFIED.

## External tools

Install/license MATLAB and Simulink independently. Configure official SATK and MATLAB MCP by their official instructions outside this installer. Before a real task inspect actual registered schemas and verify backend availability with separately authorized tests. Task-dependent products (Control System Toolbox, Stateflow/MATLAB Function, Simulink Test, etc.) need their own licenses. The Skill is neither a runtime nor a geometry executor. File installation cannot establish TOOLCHAIN_PASS.

## Upgrade

Matching contents are reused, missing auxiliary Skills are installed from the offline payload. Exact SHA/file equality defines compatibility in this release. A different auxiliary Skill stops with DEPENDENCY_CONFLICT; resolve deliberately instead of silently upgrading. A different main Skill prints differing/missing/extra files and requires YES before replacing the full directory. No production config or unrelated Skill is changed.

All payload files are staged/verified before Skill switches. Each change and backup is recorded under CODEX_HOME/.acm-installer/transaction, outside the discovery root. Multiple directory operations are not atomic; the journal and verified backups support failure recovery.

## Rollback / uninstall this transaction

Run rollback.bat, paste the exact receipt.json path (without quotes), or use:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\installer\rollback.ps1 -Receipt "<actual receipt.json path>"
```

It reverses only the receipt's changes, quarantines the new installation and restores verified complete backups. Previously reused dependencies and unrelated Skills are untouched. If the user changed an installed object after installation, rollback stops instead of discarding their work. Do not force-reinstall over a ROLLBACK_BLOCKED state; retain the journal and seek support. No history is deleted.

## Security and policy

PowerShell's process-only ExecutionPolicy Bypass does not change machine policy. If enterprise policy or signing restrictions block it, stop and contact the administrator; never disable security software. Do not run as administrator. The unsigned SHA list detects corruption but is not publisher authentication: obtain it through a trusted channel.

## Maintainer/source checkout

Source checkout installation is deliberately not the end-user flow. Maintainers run `python scripts/check_release.py` then `python scripts/build_release.py`; extract dist/Installer.zip and use its install.bat. Python is a build/test dependency only, never a recipient requirement. The default installer needs no network. Explicit Online mode is optional, pinned to official commits, and fails before Skill writes when unavailable; its successful download path has not been separately certified.
