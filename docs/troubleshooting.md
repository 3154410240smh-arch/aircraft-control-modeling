# Troubleshooting

| Symptom | Action |
|---|---|
| PACKAGE_FAIL / hash mismatch | Stop; verify SHA from trusted release and re-download. Never skip checks. |
| DEPENDENCY_CONFLICT | Preserve installed version; compare frozen manifest and coordinate a deliberate version choice. No automatic upgrade. |
| MAIN_CONFLICT | Review file hashes/extra files; only approve YES if a full backed-up upgrade is intended. |
| Permission/space failure | Use a writable current-user local path and free space. Do not disable security or elevate to bypass policy. |
| Download failure in Online mode | Retain receipt; use the complete offline Release ZIP or repair network separately. No fallback to latest. |
| ROLLBACK_BLOCKED | Preserve journal/backups/current files; user edits or uncertain ownership prevent forced recovery. |
| Source checkout missing manifest | Build scripts/build_release.py, then extract/run the named installer ZIP. |
| Installed files but old Skill in chat | Start a new Codex session/restart via supported UI and verify actual discovered path; do not edit configs blindly. |
| No MATLAB tool / missing logs | File installation is not toolchain setup. Inspect live schema and actual observability with task authorization. Stop instead of assuming simulation data exists. |

Sanitize paths, personal data, tokens, Grants and configs before attaching logs to an issue. See [SECURITY.md](../SECURITY.md) for confidential reports.
