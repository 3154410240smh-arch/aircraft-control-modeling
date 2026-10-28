# Accepted local-hover three-axis LQI case (sanitized summary)

This is evidence for the workflow candidate, not a full public Simulink project or a fresh CI simulation. The original private model/raw logs/internal paths are deliberately omitted. The two included MATLAB algebra functions are byte-identical to the accepted source; they require explicit caller-supplied arrays and contain no hidden continuous state. Their independent tests were performed in the original engineering run, not re-executed for this release.

Model assumptions: local small-angle FLU body-frame attitude, ideal feedback, no translation/full Euler transform/airframe aerodynamics; 15 degree local envelope. Physical motor dynamics and limits remain outside algorithm functions. ETH Zurich ASL RotorS Hummingbird public parameters were used with explicitly documented point-rotor inertia and symmetric motor-lag approximations, not as a claim of full RotorS fidelity.

Source: https://github.com/ethz-asl/rotors_simulator/blob/master/rotors_description/urdf/hummingbird.xacro . No upstream source code/file is copied here. The accepted private parameter snapshot and its hash belong to the original case evidence.

| Evidence | Recorded result |
|---|---|
| Augmented controllability | rank 9 |
| Riccati relative residual | 2.16407e-14 |
| Normal / rejection algorithm tests | 68 / 8, PASS |
| Corrected model cases | roll 5°, pitch 5°, yaw 8°, combined [5,-4,6]°, combined disturbance, fine-step repeat |
| Combined disturbance [3,3.6) s | [0.005,-0.004,0.002] N m |
| Disturbance peak attitude deviation | approximately [0.108609,0.086889,0.179494]° |
| Yaw recovery after disturbance | approximately 0.846 s |
| Actual motor speed range | 441.579252–464.578404 rad/s; saturation not activated |
| 1 ms versus 0.5 ms attitude difference | 5.20278e-12 rad, full timeline incl. events |
| Geometry | 46 blocks, 38 networks, 44 complete consumer paths; checked actual geometry and native visuals |
| Save/reload | per-consumer normalized paths, block parameters and function interfaces preserved |
| Independent recovered process | 13 signals matched primary result pointwise in the accepted run |

Original engineering report SHA-256: `9f6ec919c255df9b18f6d89a1f70e8b2d963757eb712c41decbd6ee92c7c092c`.
Original accepted model SHA-256 (not distributed here): `d24899e0b550bf0aa6c049be14b35714b4cd6cb6df2897a82b5a72e295c9df56`.

The initial integral bound caused yaw FAIL; a stop-gate variable collision permitted three dependent runs; compiler cache files appeared outside the intended project directory. Those failures remain failures. The corrected final case retained gains/acceptance thresholds, derived feasible integral limits, tested stop rejection and restored protected package integrity. No general model-layout reliability or saturation/full-6DOF/real-flight guarantee follows.

Project-authored source: Apache-2.0. This directory contains no commercial binaries or licenses to MATLAB. See [limitations](../../docs/limitations.md).
