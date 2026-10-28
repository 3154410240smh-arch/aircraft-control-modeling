# aircraft-control-modeling

[中文说明](README.zh-CN.md) · [Installation](docs/installation.md) · [Limitations](docs/limitations.md)

An engineering-first agent workflow for AI-assisted MATLAB/Simulink aircraft-control modeling, with explicit verification of model structure, geometry, and persistence.

**v2.5.1-rc1 is a pre-release.** It is an accepted development candidate, separate from the existing production v2.5 baseline. This repository does not silently update a production installation.

## What it does

- Turns aircraft-control requirements into functional architecture, native Simulink blocks, observable signals and bounded verification tasks.
- Selects Sum/Gain/Product/Fcn for simple algebra; evaluates MATLAB Function for matrix feedback, allocation, observers or branching algorithms when it improves maintainability.
- Keeps actuator physics, continuous states, limits and meaningful functional boundaries explicit.
- Checks actual tool schemas, authorization, partial edits, complete producer/consumer topology, geometry, native visuals, simulation data, persistence and independent recovery.

It is **not** a universal layout engine, a flight-certified controller, or a substitute for MATLAB/toolbox licenses and engineering judgment.

## Windows one-click installation

1. Open the [v2.5.1-rc1 pre-release](https://github.com/3154410240smh-arch/aircraft-control-modeling/releases/tag/v2.5.1-rc1).
2. Download `Aircraft-Control-Modeling-v2.5.1-rc1-Installer.zip` and `SHA256SUMS.txt`. Verify the ZIP hash using Windows `certutil -hashfile <zip> SHA256`.
3. Extract the ZIP fully; double-click **install.bat** (安装.bat is an equivalent entry).
4. Review the result and receipt. Run `verify.bat`; restart/new-session Codex using its supported UI and explicitly request `$aircraft-control-modeling`.

No Python, Git or administrator rights are needed to use the release installer. It uses Windows PowerShell 5.1+ and supports paths containing spaces and Chinese characters. Use the Release asset; GitHub's automatically generated **Source code.zip** is a source checkout and must first be built.

Installation is offline by default: the main Skill, 2 required auxiliary Skills and 9 verified conditional Skills are bundled. Exact content is pinned, not “latest”. Conflicting dependencies stop without overwriting; a different main Skill requires explicit confirmation and full backup. Six additional specialist routes are unbundled because their precise source version was not frozen; only those tasks remain conditional/blockable. See [dependency policy](docs/dependency-policy.md).

## Toolchain preparation

You independently need licensed MATLAB/Simulink and compatible SATK/MATLAB MCP tooling exposing the required live schema. Control System Toolbox, Stateflow/MATLAB Function and other products are task-specific requirements. The installer does **not** install or configure these, change config.toml, register a geometry executor, or grant model-write authority. [Compatibility](docs/compatibility.md)

## Evidence and boundaries

The corrected three-axis hover-near LQI case used two MATLAB Function algorithm blocks with native physical dynamics. Its private engineering acceptance recorded 68 normal algorithm tests, 8 rejection tests, six corrected simulations and one independent recovered-model run, plus topology/geometry/persistence checks. Earlier integral-bound, stop-gate and cache-scope failures remain acknowledged. This release includes a [sanitized case summary and two exact algorithm sources](examples/quadrotor-lqi/README.md), not private models, raw experiment logs or a new claim of hosted reproduction.

No general guarantee is made for arbitrary Simulink models, complex branches, label bounding boxes, saturation-excited full loops or full 6DOF aircraft. N-LEAF, uncertified complex routing/Points edits and arbitrary universal layout remain unavailable; native geometry profiles depend on separately certified tooling. [Architecture](docs/architecture.md) · [Known limitations](docs/limitations.md)

## Verify, upgrade and roll back

`verify.bat` re-reads installed files and hashes. Logs/backups are outside the skills discovery directory. Re-running an identical package reuses matching files. Main upgrades show differences and require `YES`; auxiliary differences block instead of silently changing versions. `rollback.bat` accepts the recorded receipt path and reverses only this transaction. It refuses to overwrite later user edits; reused dependencies and unrelated Skills remain untouched. [Full instructions](docs/installation.md) · [Troubleshooting](docs/troubleshooting.md)

## Development and releases

The minimal build/check/test scripts use Python's standard library for maintainers only. `python scripts/check_release.py`, `python scripts/build_release.py`, then on Windows `python tests/installer/test_install.py --package <extracted-release-root>`. CI runs source, package and isolated Windows installer checks; CI does not run MATLAB or establish recipient toolchain health. [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [Support](SUPPORT.md)

Report sanitized reproducible issues through GitHub Issues; follow [SECURITY.md](SECURITY.md) for sensitive vulnerabilities. Updates are explicit versioned pre-releases until broader acceptance is complete.

## License

Project-authored content: [Apache-2.0](LICENSE), copyright 2026 Tide827. Bundled MathWorks Skills retain their separate restricted-use redistribution licenses; see [NOTICE](NOTICE) and [dependency manifest](manifests/dependencies.json). No commercial software license is included.
