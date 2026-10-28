# v2.5.1-rc1 release audit

## Identity and freeze

This is the accepted independent algorithm-selection candidate, not the separate production v2.5 baseline. Its six main file hashes are frozen in manifests/candidate-baseline.json and validated before building; no candidate rule has been rewritten for publication. The original engineering report fingerprint and bounded case results are summarized in examples/quadrotor-lqi/README.md without private paths/raw logs.

## License and privacy

The project owner explicitly confirmed rights and Apache-2.0 permission with attribution Tide827 (2026). MathWorks auxiliary files retain their original license conditions and notices, including MathWorks-product/service-only use. They are not relicensed as Apache or represented as unrestricted BSD. Eleven bundled auxiliary Skills were matched file-by-file to official immutable Git commits; six unresolved conditional routes are excluded, with no guessed substitutes.

No production config, runtime Grant/key, commercial executable, toolbox, private model or personal logs are included. Source and archive scans reject personal host paths, common private-email patterns, key markers and token-like values. This is a review aid, not proof that all possible secrets can be recognized automatically. A fresh Git history is created from reviewed publication files only.

## Checks and limits

Source/package checks cover required files, exact main/dependency hashes, fixed source commits, preserved notices, local Markdown links, Skill reference paths, source formatting, secret patterns, package manifest/CRC and exact extracted content. PowerShell parser and isolated Windows install/rollback tests are separate. GitHub CI reuses these portable checks with read-only contents permission and a pinned checkout action; no MATLAB or hosted flight-control validation is claimed.

Formatting checks preserve byte-identical upstream third-party Markdown, including its original hard-break/trailing whitespace. The third-party whitespace attribute is explicit; project-authored Markdown is checked strictly. No accepted Skill or official file is rewritten merely to normalize formatting.

Git attributes explicitly recognize CRLF as a valid line ending while disabling automatic byte conversion. This prevents a Windows carriage return from being mistaken for trailing content and keeps frozen file hashes stable across checkout platforms.

The release-stage audit requires actual final-ZIP Windows results and post-upload anonymous download/hash/CRC verification before PUBLISHED_PRE_RELEASE may be reported. File installation, Codex metadata discovery, current desktop activation and external toolchain health remain different conclusions. See tests/INSTALLATION_TEST_REPORT.md and docs/limitations.md.

Release asset filenames use ASCII so that GitHub filename normalization cannot invalidate the published checksum list; the usage document remains Chinese in content, and the repository retains README.zh-CN.md. The archive itself still contains its Chinese installation entry and supports Chinese filesystem paths.

## Recovery and safety

The installer uses complete verified staging, explicit main replacement approval, full old-directory backup outside skills, persistent receipts/events and object-scoped rollback. Dependency conflicts fail rather than silently upgrade. Reused/unrelated Skills are not removed, later user edits block destructive rollback. No recipient production config or model permission is changed.

N-LEAF, arbitrary universal geometry, uncertified complex branch repair and unverified capability profiles remain unavailable. Public release is pre-release only; broader platform, recipient activation/toolchain and independent real-task acceptance are needed before stable status. No Token savings or universal performance benefit is claimed.
