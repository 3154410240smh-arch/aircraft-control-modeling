# Applicability-driven verification and recovery

## 1. Evidence contract and independent oracle

正式验收在一份权威配置中固定条件/阈值；脚本、报告与图表读取或引用同一版本，不各自维护阈值。每项结果绑定：

| 字段 | 必须明确的含义 |
| --- | --- |
| 信号 | 被测对象、物理语义、单位；单轴/分量/范数；需求、预测、静态可实现或动态实际 |
| 时间 | 原始时戳、采样阶段、对齐/保持/插值方法、统计窗口及统计方法 |
| 判据 | 配置来源/版本、容差、独立oracle、假设和适用范围 |
| 版本与运行 | 模型/算法/参数冻结标识或哈希、执行模式、依赖及结果路径 |
| 缺项 | 缺失字段、未运行项目与因此不能支持的结论 |

不为填字段而捏造数据；关键证据缺失使对应结论UNVERIFIED，已明确违反门限则FAIL。测试结果状态与根因置信度分开：CONFIRMED有直接证据、LIKELY有较强间接证据、UNVERIFIED缺关键证据、RULED OUT有排除依据。局部、短时或同输入一致性不能提升为完整闭环/因果/部署结论。

Prefer, in order and conditioned on matching assumptions:
1. User-provided confirmed reference values and independently specified requirements.
2. Analytic physical laws / known-answer cases developed independently of the implemented block equations (e.g. rotor `r cross F`).
3. Official trusted examples or validation datasets with matched versions and conventions.
4. Independently implemented alternative calculations with clearly documented shared assumptions.
5. Formula/result directly reused from the component being tested: **low independence**, useful only for consistency, not for claiming independent physical validation.

Each applied test records `case`, `scope`, `applicability rationale`, `oracle`, `assumptions`, `tolerance`, `result path` and `PASS|FAIL|UNVERIFIED`. Don't generate extra plant models when tests don't apply.

本文件选择技术上必要的验证，不授予运行权限。只读/局部编辑授权不隐含编译或仿真；缺少必要操作授权时仅申请该操作，保留未验证结果。文档、静态推演、独立Agent离线决策与实际模型运行分别标注，不能相互冒充。

### 1.1 观测闭合门禁

仅在任务需要数值指标/实际时序证据时激活：由验收指标反推最小必要信号集，固定真实源端口、完整消费关系、作用域、物理语义/单位、记录名、数据形状及时间覆盖/采样阶段。可在已批准的实际输出上推导误差，但必须事先声明公式与独立性，不能假冒额外实测通道。SignalLogging、端口记录开关、有效覆盖配置及输出容器是不同层次。

仿真前复用当前有效结构证据，按真实作用域配置并读取实际记录状态、模型级开关、名称和抽取/点数限制；有效覆盖方案须由当前契约支持并可核验。ok、日志图标或编译通过均不是充分证据。缺少必需通道或无法确认生效则BLOCKED，不先花一次仿真赌输出；缺合规入口不得裸API补写。具体日志接口证据按需查local-toolchain.md §6。

不默认增加探针仿真：首个既定代表工况兼作实际输出门禁，先保存真实SimulationOutput，再检查其实际包含的容器（如约定logsout、yout或获准记录通道）、名称、形状、有限性及每路全时段/事件时刻覆盖，之后才继续后续运行。若必要数据缺失，记录验收FAIL、相关控制指标UNVERIFIED，停止依赖运行；已经发生的仿真仍计预算，不能只凭SimulationMetadata完成转为数值PASS。输出通道与配置/会话改变时重核受影响证据，未变证据不重复采集。

### 1.2 函数式算法门禁（涉及算法块时）

实现前冻结函数接口、参数、类型/维度、采样及显式状态；将源代码与实际块内代码绑定哈希。实际执行零输入、正负方向、多轴组合、边界与异常维度用例，对照独立参考方程；混控另用几何力臂/反扭矩核对正反映射和可实现约束。不得用同一函数自我调用当独立oracle。需要时对病例停止门禁做一次失败注入，确认FAIL/UNVERIFIED后依赖运行数为零；不能只相信脚本中写有error语句，调用者命名空间遮蔽也须防止。离线函数通过不代替块编译、实际时序输出、闭环与持久化验收。保存重载需复查块内代码、接口、参数及更新语义；缺项或FAIL沿用现有停止规则，不调低门槛。

## 2. Checks are distinct

- **Structural:** expected blocks, directions, ports, topologies and compatible configuration.
- **Update/compile:** dimensions, data types, parameters, solver/sample-time diagnostics.
- **Run:** simulation completes with valid finite relevant outputs.
- **Physical known-answer:** applicable motion laws, force/moment signs, frame identities, and actuator mapping independent of the implementation.
- **Trim:** selected flight condition, constraints, residual, drift and consistent internal state.
- **Control:** designated closed-loop performance and actuator/state constraints.
- **Robustness:** only the disturbances/failures/uncertainty envelope actually covered.
- **Reproducibility:** independently started MATLAB session when warranted by change risk.
- **Numerics:** relevant precision/sensitivity, original time/phase alignment and finite states; reproducible coarse results alone do not establish convergence.
- **Computational burden / deployment:** frozen code and execution mode, timing boundary, cold/warm entry, load and tails; simulation/desktop speed is not target-hardware real-time evidence.

Do not mark later checks PASS merely because earlier checks passed.

## 3. Change-to-test defaults (extend only for dependencies or risk)

| Change | Minimal applicable tests | Escalate when |
| --- | --- | --- |
| Comments, scope titles or visual-only layout | Confirm unchanged endpoints, topology, parameters and semantics; inspect affected diagram | Connections, ports, parameters or execution semantics changed: structural check and impacted functional tests; position-only moves do not automatically trigger simulation |
| Direct/Goto/From/Bus representation or interface organization | Freeze original contract (new model: specification); scoped expanded source-consumer, signal and physical mapping checks via §8 | Types/dimensions/timing/port/log impacts: authorized compile and minimal affected functional tests; not an automatic full suite |
| 功能层级/布局架构调整 | §8中适用的完整拓扑、功能分区、接口空间、几何、视觉及保护范围检查 | 层级、接口或日志影响执行/类型/时序时，授权范围内编译与最小功能回归；不把纯Position默认升级为全套仿真 |
| Chinese display/annotation | Meaning, readability and unchanged technical identities/interfaces in affected region | Actual renaming or script/log/bus/codegen dependency: scoped compatibility and impacted tests |
| 日志/输出记录配置 | §1.1必要信号与实际状态闭合，核对保护对象；首个既定运行核对真实输出 | 容器/时序/依赖变化时验证受影响指标；仅日志修改不默认全布局或额外仿真 |
| PID/controller gains | Numeric parameter validity, affected closed-loop response, actuator/state bounds | Changed equilibrium/coupling or formal release: integrated scenarios |
| Mass, inertia, aero or propulsion constants | Units/physical plausibility, corresponding known-answer dynamics, trim where impacted, closed-loop regression | Large deviations or validity envelope shift: additional modes/precision |
| Controller sample period or solver | Update/compile, rate conversion/order, affected loop response, numerics as needed | Solver-sensitive outputs: step/tolerance study |
| Rotor allocation, motor numbering/rotation | Independent lever-arm and reaction torque signs, attainable wrench/actuator limits, affected closed-loop behavior | New motor configuration: all relevant axes |
| Native block type/port/interface | Installed-version semantics, structure, update/compile, affected physical signal tests | New dynamics: independent physics and trim as needed |
| Plant structure / new dynamics | Structure, compile, short run, matching independent physics tests | Formal closed-loop design: trim and control validation |
| Initialization or workspace dependencies | Initialize in clean context, representative run | New complete project/formal evidence: clean MATLAB session replay |
| New full deliverable | All critical task-specific tests and reproducibility | Robustness/fault testing if task explicitly requires it |
| Custom observer / evaluator | Interface contract, valid committed records, fault latch and scoped baseline comparison | Runtime evidence needed: load runtime-diagnostics.md; failure blocks related conclusions |

A pre-existing linear state-space LQR controller project does **not** require tests for 6DOF gravity, motor allocation or quaternions unless those components are part of the scoped deliverable.

新增/修改限速、饱和、查表、模式切换等非光滑环节，在线优化/非线性分配，混合时序或已知步长敏感性时，在昂贵独立工况消费前做有界代表性数值检查；沿实际会触发的边界核对传播、对齐及步长/容差。最终冻结版本仍做约定的适用数值验收，不能用早期检查代替。普通增益、纯视觉或低风险改动不默认全量步长复验；出现新敏感性才升级。

早期关键检查失败先限制诊断，不继续用独立工况补报告。冻结后的独立数据一旦参与设计，明确新迭代及新的未用工况，核对设计与额外运行是否已有授权，缺少才申请；不得继续称旧数据独立。不为省调用取消必要独立验证。

### 3.1 事件感知的精度合同

精度运行前区分参考/模式的真实跳变、饱和边界等非光滑事件与应连续的状态/执行机构输出；饱和切换不必然造成输出跳变。记录实际可能触发的事件、求解器/保持与积分阶段、原始时戳及同物理时刻对齐规则。固定全时域硬指标的信号、单位、最大差/RMS等所需统计及容差；若任务还需连续区间或事件局部诊断，另行预置窗口/端点与比较方式，不能把两类指标混为一个PASS。事件位置相同、响应曲线接近或名义系统稳定都不能替代完整对象的数值验收。

全时域硬判据仍覆盖事件，除非需求在运行前明确批准其他定义。事件局部异常先用已有时序定位最早有意义差异、峰值时刻、输入/限幅/实际状态和数值关系，不自动加跑求解器实验。事后诊断窗口必须标为探索性，不能删除事件样本、平移轨迹、改插值或改门限以追溯覆盖原FAIL；连续区间通过也不抵消全时域失败。数值关系吻合与已观测到求解器内部阶段是不同证据等级。需要更改算法/求解器或正式精度定义时，按G0/G1检查授权，保留原失败与配置版本。

## 4. Recovery tiers

- **L1 (each edit scope):** inspect returned tool status and actual changed topology; immediately run the installed editor's required `model_read` after any `partial` response, reconcile actual state, and use an additional checker only when actually exposed/required. Otherwise inspect available topology/port evidence; never fabricate a `model_check` tool. No complete-file snapshot required per routine edit.
- **L2 (functional milestone):** save a verified working state when a usable subsystem/feature has passed its relevant checks.
- **L3 (major milestone):** retain a recoverable stable engineering baseline after important plant or closed-loop validation.
- **Risk escalation:** make an extra backup before deleting/renaming large subsystem(s), replacing controllers, changing model references, or other high-impact operations.

Protect original files. Recover both model and relevant parameters/initialization dependencies. This is an engineering recovery procedure, *not* an atomic transaction guarantee.

## 5. Clean replay and result statuses

Clean-session replay is default for first complete model delivery, changed initialization/critical dependencies, major model structure refactoring, and formal scientific results. For low-risk changes, run scoped regression and record which previous baseline passed full replay; never imply a newly altered model has passed the older test if it hasn't.

- `PASS`: performed test with evidence and defined tolerance met.
- `FAIL`: test performed but criteria failed, including constraint violations.
- `UNVERIFIED`: not run, unavailable hardware/software, missing oracle or insufficient evidence.
- `N/A`: genuinely outside this change/test scope, with reason; not PASS and not a substitute for missing required evidence or authority.
- `BLOCKED`: an explicit prerequisite prevents the affected stage; do not broaden authorization or bypass the tool contract.

功能/控制、数值精度和文件交付分别给状态；只有合同全部适用硬项通过才给综合PASS。控制性能PASS而精度FAIL时综合仍FAIL；未执行的保存重载/视觉/依赖恢复为UNVERIFIED，不因数值失败自动记N/A。任何适用硬项已有实测FAIL，不把整体降写为只有BLOCKED；缺必要前提时阻断对应阶段并注明原因。停止下游验收不隐含禁止已经获准的安全归档/恢复，但失败归档不得包装为通过版。

交付明确区分内存与磁盘：最后一次实际Dirty/加载身份、实际保存路径和SHA、哪些配置仍只在会话或SimulationInput生效、原参数/依赖及复现入口限制。没有保存重载证据不能称修复已持久化；已有备份不等于实际恢复通过。恢复与安全关闭只限获准副本，不为完成报告覆盖用户原件。

Include environment fingerprint, source model version/checkpoint, tests, raw outputs/metrics as relevant, limitations, reproduction instructions. Avoid dumping verbose raw logs into chat; retain locally as needed.

If a critical check fails, stop stacking edits, inspect actual state and repair only within authorized scope/budget. When state cannot be trusted, undo the candidate or restore the verified model and matching parameter/init dependencies under the recovery authorization; if that authority is missing, protect evidence and request that specific operation. Missing tooling blocks the affected stage, not a PASS. Directory moves and tool calls are not assumed atomic; verify the recovered file set/state before resuming.

## 6. Stage budgets and minimal sufficient operations

复杂任务先明确目标/可证伪假设、已有与缺失证据、允许的修改/工具、实验/求解/时间/数据预算及成功/失败/停止条件。函数调用、内部求解、仿真尝试、编译、工具请求分别计数并注明来源；未测量的内部量不能从外层次数冒充实测。容量按有依据的事件率和载荷估计，不按控制帧名义数猜；未知时先提出获准的短测。

预算在首个相关操作前按实际调用链合计：能力/会话前检、基线读取、各作用域构建与日志配置、每批专业Skill要求的即时读取、实际记录状态及必要保护快照、首个与其余工况、精度复验、原生图、保存重载、依赖恢复和最终文件核查。作用域数决定配置批次下限，不能把多个层级塞进一次编辑。先定义取证事务边界并展开到外层调用；结构读取和独立快照分别执行就分别计数，不到执行中再把它们打包缩数。合并同检查点字段/复用匹配证据不能省略专业Skill强制读取。

为完整适用验收和已获准恢复保留额度；预算若连必需阶段都不够，在编辑/运行前说明最小缺口，不先留下半配置模型。失败调用、无日志运行和恢复不退回额度；是否有一次有限重试及其停止点必须预先明确，不能围绕同一日志故障反复追加预算。纯理论/只读任务不因此启动运行检查；安全必需项缺预算仍须停止，不以节省Token为由漏检。

失败先分类：结构/拓扑；参数/初始化/工作区；物理/算法/控制设计；积分/时序/求解器/编译；接口/连接/版本；观测器；验收程序/标准。证据链记录“现象→最早有效差异→模块/信号→机制→替代解释→置信度”，不从单个错误字符串确认根因。已有证据足够就停止；前提未变不重复同一错误。修复重试仅限授权和剩余预算；超出或核心路线实质变化时内部复审，只对必要决策申请新授权，不重交整份审批表。未闭合报告最小缺项，不无限排障。

复用未变的Skill/模型图和版本证据；接口或配置变更使相关缓存失效。有限批量查询同作用域参数，先估计返回规模；复用已取得编译结果，不为逐字段查询重复编译。局部编辑只核查影响范围，partial恢复要求不因缓存省略。

日志保留原始结果和必要窗口明细，向用户返回短摘要及路径，避免长日志进上下文；不为形式完整重复读取/导图/全轨迹重跑。官方工具不适用时记录失败，选择授权且独立可核实的替代，不把替代成功写成原接口已修复。性能分析复用本机相关Skill，不因源码重复表达式直接宣称运行瓶颈或加速比例。

## 7. Workflow stage contract

工程任务按下表形成最小可追溯链，可合并简单步骤；不适用阶段记录原因，未授权的必要验证保留UNVERIFIED。理论直接回答，不强制保存工程阶段表；复杂任务将阶段/版本/证据/状态保存在简短记录中，不重复输出全文。编辑前保护源文件/依赖基线，与全部构建完成后冻结的初始布局基线是两个检查点；各次编辑仍执行L1，中间状态不编译/运行冒充完整实现。内存Dirty状态、已保存文件及稳定检查点分别记录。

| 阶段 | 进入条件 | 执行条件与动作 | 退出证据 | 失败/缺项处理 |
| --- | --- | --- | --- | --- |
| 任务理解 | 用户请求 | 区分结果、对象、只读/修改/运行边界与事实/假设 | 明确任务类型及交付 | 先查授权证据，关键歧义才问 |
| G0内部审查 | 类型与范围已识别 | 评估风险级、关键输入、具体授权、路线、预算及停止/恢复 | 最小内部计划；复用有效批准 | 只就缺项/授权/异常/实质变化交互 |
| G1技术预检 | 下一操作有授权 | 当前专业Skill/schema/会话/副作用检查；不默认初始化 | 所需能力和门禁证据 | 不猜参或绕过，阻断受影响操作 |
| 基线冻结 | 即将修改或正式对照 | 保存作用域、源版本、依赖和必要检查点；保护原件 | 可恢复且可追溯的基线 | 版本不符停止，不自行覆盖/恢复 |
| 规格 | 最低保真度与已知输入 | 固定坐标/单位、状态、限制、工况和权威判据 | 可检查接口/标准及假设 | 缺物理参数不虚构；非关键缺项注明 |
| 执行规划 | 规格充分 | 变化→最小验证；含观测、事件精度及交付/恢复的总预算，原生优先 | 每步有目标/影响/检查及授权，必要信号可配置和取证 | 预算/能力不足先说明缺口，不先消费依赖运行 |
| 受控实施 | G1、授权及基线有效 | 仅受控工具与既定作用域，部分成功非原子 | 真实工具结果/修改范围 | 异常停叠加，保留错误转即时核查 |
| 即时核查 | 每个编辑结果/partial | 读实际状态、端口/参数/连接，不只信成功消息 | L1一致；需要时L2里程碑 | 局部修复/撤销；不可信按授权恢复 |
| 影响验证 | 实际变化已核实 | 按§3最小充分集；非光滑风险数值前置 | 分层状态及原始证据 | 不改阈值；失败限制诊断，不消费独立数据 |
| 独立验收 | 参数/算法冻结、对应运行获准 | 适用独立oracle/未用工况及风险驱动复现 | 独立证据与适用边界 | 未运行UNVERIFIED；参与设计则重新标记 |
| 交付/恢复记录 | 已达结论或停止条件 | 实际产物/依赖/结果/缺项/成本和恢复位置 | 可复查交付及原件保护状态 | 不完整亦如实交付，不扩展未授权实验 |


## 8. Line routing persistence and file recovery

Q01–Q14是变化与风险驱动的验证矩阵，不是每个任务全部执行的流水线。先用已有规格/差分确定适用项、作用域和证据；安全关键的适用项必须执行或复用仍有效的匹配证据，缺授权/工具/数据为UNVERIFIED并阻断依赖结论（明确不能继续时BLOCKED），不能记N/A。真正无关项记N/A并注明理由，不算PASS；不为填表新增模型查询、编译/仿真或恢复演练。此规则不削弱G0/G1或官方编辑器要求。

| 项 | 激活条件 | 最低证据 |
| --- | --- | --- |
| Q01 授权/工具 | 任一实际操作前 | 目标/副作用/授权、当前专业契约；复用未变证据 |
| Q02 逻辑拓扑 | 新建连接、受影响信号/连接/表示 | 新建对规格；既有对原契约，展开标签/Bus后源与全部消费者一致 |
| Q03 物理表示 | 模型结构或几何编辑 | 仅白名单差分；纯几何拓扑不变 |
| Q04 信号契约 | 新接口、表示/类型/维度/时序可能受影响 | 单位/坐标/类型/维度/采样阶段；必要编译另核授权，复用已有结果 |
| Q05 标签 | 作用域内Goto/From新建、改动或解析受影响 | 唯一正确源、可见域和完整消费者；适用规范配置 |
| Q06 Bus | Bus/元素/接口或映射受影响 | 元素全集、类型/维度/时间语义及消费映射 |
| Q07 因果追踪 | 关键链/反馈/结构接口组织受影响 | 真实关系及双向反馈可追踪，不用假穿通 |
| Q08 块/状态 | 任一模型编辑 | 核对受影响和保护边界内身份、参数、初值、技术接口及允许位置/方向差分 |
| Q09 几何/邻区 | 位置/线路/显示或表示布局变化 | 全目标/邻网、块矩形、端口/引线、逐消费者路径及文字预留，无新穿块/遮挡/越界；原生图核验实际显示，不虚构字形边界 |
| Q10 改善 | 声称布局优化/改善 | 预置目标至少一项真实改善，其他硬项不退化；无变化仅无退化 |
| Q11 V2 | 保存交付、持久化能力验收或重载风险 | 只保存/关闭自己的授权副本，重载重解逻辑/几何，固定容差 |
| Q12 V3 | 布局/中文显示或视觉改善结论 | 同条件原生图、关键路径/反馈/标签检查；缺图不认证 |
| Q13 F1 | 高影响/复杂分支或接口风险、恢复异常、新恢复能力/正式持久化验收 | 匹配不可变文件/依赖基线；实际恢复触发时全SHA及会话身份核对，匹配证据可复用 |
| Q14 功能/数值 | 新完整模型、信号语义/执行/依赖风险或正式回归 | §3最小充分集及原阈值；纯位置不默认仿真，不改增益掩盖差异 |

既有模型表示转换执行前，Q01/Q03/Q08/Q09须覆盖自动布局的潜在影响域：先有可靠限制证据，或对已界定影响域的事前区域授权及验收能力；无法界定/控制时BLOCKED，不以一次试改代替前置证明。incremental不作位置冻结证据。逻辑图一致只能支持Q02，不能替代几何、编译/功能、V2或F1；Bus及未经实测的新建工作流保留UNVERIFIED。安全门禁FAIL立即停下游验证与叠加编辑，保留既有FAIL，不因规则部署重新标PASS。

只读设计不执行编辑后/V2/F1测试；已有模型纯几何一般激活Q01/Q02/Q03/Q07（关键路径受影响时）/Q08/Q09，主张改善再加Q10/Q12，保存交付加Q11。标签或Bus表示改造再激活Q04/Q05或Q06及相应Q07/Q14；不是自动启动全工况。普通PID按§3检查参数和受影响闭环/约束，不因此加载全布局矩阵。新建按规格核对首次实现，不要求先直接连线再转表示。

分别冻结语义和几何：稳定源/完整目标/扇出、功能块与信号契约；位置/方向、路径/junction、标签、邻区和截图。获准表示改造另存物理白名单及展开逻辑映射，不能用“物理图必须相同”否定合法变更，也不能用逻辑等价放过越界几何。V1即时、V2保存重载、V3原生视觉、F1文件恢复分别按激活范围给PASS/FAIL/UNVERIFIED或N/A，互不代替。

取证路径须能覆盖实际作用域：model_read用于结构，不能单独替代完整分支树、逐消费者Points、端口锚点与原生图。复用取证代码前审查直接/间接函数依赖、真实消费者遍历、读写及回调副作用；只在授权副本、授权只读执行入口采集，证据文件写入不隐含模型或显示状态修改许可。记录字体继承设置和原生图的窗口/缩放等条件，不假装取得未测文字包围盒；图像不足以判断硬约束时该项UNVERIFIED并停止依赖操作。不能用继承字体测量失败代替所有视觉能力失败，也不能以保守预留宣称实际显示通过。

布局放行须有实际架构/拓扑、几何/保护、标签/原生视觉及适用编译/功能证据；保存交付再验证重载，恢复按Q13执行。若根级候选仍有一次获准整理无法处理的硬缺陷或预检无安全候选，停止该路线，不连续补偿；设计约束、有限案例能力证据和本次运行结果分开，静态规则通过不等于布局能力通过。

预先固定影响区、几何规范化/容差、目标冲突和截图条件。routeLine专项块身份/位置/尺寸/方向/参数/接口不变，完整拓扑一致；区外无未授权变化，不新增穿块、端口遮挡/冲突。有已知冲突须至少改善一个，否则不能称优化成功。等价线段规范化仍须验证属性/阅读性，不事后放宽。高级路由未验证范围继续禁用。

异常/partial/超时或状态不明立即停叠加，保留原请求/故障，先读实际状态，不换request_id重试、不写Points冒充恢复。按获准范围安全关闭仅自己的受影响副本，隔离故障，从不可变基线恢复匹配文件/依赖并核验SHA及加载身份；恢复不明停止，不保存其他共享模型、不默认删除故障。重载/编辑/改线/会话或接口改变使相关句柄和缓存失效，未变证据复用。

预算不叠加：先单次功能门禁；通过且另需效率研究时，每方法每用例5个独立副本，同环境/输入/授权/质量标准，报告中位数/四分位距及冷/热。外层调用/原生调用/编译/仿真/恢复分记，时间不重复相加。20%时间与30%无效重复降低仍为拟议目标，缺真实Token/视觉/样本则UNVERIFIED，不追加无关运行。RT0–RT6仅为布局实验编号；L1–L3始终只表示§4恢复检查点。
