# Dependency and redistribution policy

The release bundles 2 required Skills (building-simulink-models and simulating-simulink-models) and 9 proven conditional Skills. All bundled files were byte-matched to the official repository at immutable commits before redistribution. The exact names, trigger conditions, versions, paths, file SHA-256 and license notices are in [dependencies.json](../manifests/dependencies.json).

Pinned official commits: `ead4c58f4b62ba0d57fe70c80484746de07a1501` and `ef5d5f8faeca13d8c66e94828bf6a44aadaa8b3f` in https://github.com/matlab/simulink-agentic-toolkit. Older accepted content is not replaced with current repository HEAD. Every bundled original copyright/condition/disclaimer is retained in third-party/licenses and release licenses.

Their original files label a MathWorks license, but the full text additionally restricts use solely in conjunction with MathWorks products and service offerings. Do not describe them as unrestricted OSI BSD or apply the project's Apache license to them. The project is an open-source workflow with separately licensed auxiliary material; the distribution is not entirely under one open-source license.

Six conditional routes are not bundled: simulink-interactions, matlab-debugging, matlab-optimize-performance, simulink-debug-commandline, simulink-profiler-analyzer and simulink-solver-profiler-analyzer. Their precise accepted local versions lacked frozen official provenance; no guessed downloads or replacement upgrades are performed. Their absence blocks only the relevant specialist task, not the two verified core dependency files. There are no separately declared optional dependencies in this release.

MATLAB/Simulink/SATK/MCP and conditional products are external_toolchain entries, not Skill files. They require independent installation/licenses/configuration. The package never downloads binaries, executes remote setup scripts, registers an executor or configures MCP.

Offline is the default. Explicit Online mode uses fixed official raw URLs and exact file hashes; a failed download stops before Skill writes. License/source-unknown required dependencies would block publication; no such required item is claimed satisfied here without evidence.
