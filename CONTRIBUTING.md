# Contributing

Open an issue describing the engineering need before broad workflow changes. For defects provide a minimal redistributable reproduction, environment versions, actual tool schema, exact scope/operation, expected and observed behavior, sanitized error/logs, file hashes and recovery status. Never include private models, production configs, tokens, Grants or unlicensed third-party files.

Keep SKILL.md small, conditional references focused, authorization explicit and test evidence separate from plans. Preserve existing candidate hashes unless a reviewed versioned change deliberately replaces them. Do not weaken thresholds after seeing failures or silently enable uncertified native capabilities.

Run `python scripts/check_release.py`, `python scripts/build_release.py` and the isolated Windows installer suite against the extracted archive. Contributions involving MATLAB behavior need independently authorized native tests; CI source checks are not MATLAB certification.

By submitting a contribution, you confirm that you may license your original contribution under Apache-2.0. Third-party material retains its own approved license and notices. Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
