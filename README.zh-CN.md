# aircraft-control-modeling

[English](README.md) · [安装说明](docs/installation.md) · [能力边界](docs/limitations.md)

面向飞行器控制的工程化智能体工作流，强调 MATLAB/Simulink 模型构建、合理的算法实现方式、几何布局和可复现验证。

**v2.5.1-rc1 是预发布候选，不能当作稳定正式版。** 正式生产 v2.5 与该候选分别冻结，发布不覆盖开发者生产环境。

## 能解决什么问题

从控制需求出发规划功能层级、完整信号关系、监测接口、原生模块、工具授权和验证预算；检查实际编辑状态，区分结构、几何、视觉、编译、数值、保存重载和独立恢复。简单计算优先 Sum/Gain/Product/Fcn；矩阵反馈、混控等算法按可读性评估 MATLAB Function。连续积分、物理动态和限幅保持清楚的原生边界，禁止以一个函数隐藏整个模型。

## 一键安装

从 [v2.5.1-rc1 Release](https://github.com/3154410240smh-arch/aircraft-control-modeling/releases/tag/v2.5.1-rc1) 下载安装 ZIP 与 SHA256SUMS.txt，核对 SHA-256，完整解压后双击 **install.bat**（或安装.bat）。无需 Python、Git 或管理员；需要 Windows PowerShell 5.1+。不要直接运行 GitHub 自动生成的 Source code.zip，它是待构建源码。

离线包含主 Skill、2 个必需和 9 个已核实条件辅助 Skill。匹配版本复用，缺项补齐；不同辅助版本停止，主 Skill 不同必须明确确认并完整备份。另有 6 个条件路由未冻结具体来源版本，未打包或自动替代，涉及时可能 BLOCKED。安装不会自动补齐 MATLAB、Simulink、SATK、MCP、许可证或执行器。

运行 verify.bat 检查文件，再按 Codex 支持的方式重启/新开会话并明确调用 `$aircraft-control-modeling`。文件安装成功不等于当前对话已加载，不等于 MATLAB 工具链可用。[安装与回滚](docs/installation.md) · [依赖政策](docs/dependency-policy.md) · [兼容性](docs/compatibility.md)

## 实际证据与限制

修正后的悬停附近三轴 LQI 案例记录了 68 组算法数值测试、8 组拒绝测试、6 组修正版仿真及1组独立恢复会话仿真；编译、完整消费者路径、几何、原生图、保存重载及恢复在该具体案例通过。此前积分硬限、失败停止及缓存目录问题保留为真实失败，不写成一次全通过。

公开目录提供[脱敏案例摘要及两个原样算法源文件](examples/quadrotor-lqi/README.md)，不包含原始私有 SLX 或完整运行日志，不声称本次 GitHub CI 重跑了控制实验。并非完整六自由度或真实飞行器安全认证，也不是任意模型通用布局引擎。N-LEAF、未认证复杂分支路由/Points 精修及复杂文字包围盒认证不开放；原生几何能力还依赖独立工具及匹配的认证 profile。[架构](docs/architecture.md) · [已知限制](docs/limitations.md)

## 升级、故障与贡献

安装器复用完全匹配内容，主版本升级比较差异并要求 YES；日志与备份在 skills 外。rollback.bat 仅撤销 receipt 中本次修改，后续用户修改会阻止覆盖，不删除其他项目的依赖。[排障](docs/troubleshooting.md) · [贡献](CONTRIBUTING.md) · [安全](SECURITY.md) · [支持](SUPPORT.md) · [变更](CHANGELOG.md)

维护者可使用 Python 标准库执行 scripts/check_release.py、scripts/build_release.py 和隔离安装测试；接收者无需 Python。CI 只验证发布文件和安装器，不验证 MATLAB 工具链或实机控制效果。不编造 Token 节省或普适性能提升。

## 许可

项目自编内容采用 [Apache-2.0](LICENSE)，Copyright 2026 Tide827。MathWorks 辅助 Skill 保留单独许可，含“仅与 MathWorks 产品或服务结合使用”的限制，不会被主项目重许可。[NOTICE](NOTICE) 与[依赖清单](manifests/dependencies.json)列出范围；本包不提供商业软件许可。
