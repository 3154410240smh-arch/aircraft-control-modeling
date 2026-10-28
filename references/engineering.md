# Engineering contract (load when building or analyzing aircraft models)

## 1. Minimal model specification

Record for each new project or significant engineering change:

| Field | Required meaning |
| --- | --- |
| `aircraft_configuration` | Fixed wing / multirotor / VTOL; motor positions, numbering, rotation, control surfaces and axes where relevant |
| `model_fidelity` | Linear small-disturbance / simplified nonlinear / integrated nonlinear / high-fidelity; choose minimum sufficient fidelity |
| `validity_envelope` | Trim state, speed/altitude, attitude, commanded dynamics and disturbances where approximations remain justified |
| `simplifying_assumptions` | Assumed symmetry, rigid body, actuator idealization, small angles, negligible effects, etc. |
| `excluded_dynamics` | Unmodeled motors, aerodynamics, sensor/estimator, environment, structural flex, delays, etc. |
| `frames_units_signs` | Body/inertial/wind axes, altitude signs, Euler order, angular velocity, force/moment units |
| `signals` | True state `x`, measured signals `y`, estimated state `x_hat`, control demand `u_cmd`, realized actuator inputs `u_act`; map acceptance metrics to required observations and actual sources |
| `actuation` | Allocation map, attainable set, saturations, slew limits, lag, sign, trim biases |
| `solver_record` | Continuous solver or fixed-step choice; relative/absolute tolerance as applicable, max step, sample times, hold/rate transition, zero-crossing when relevant |
| `acceptance` | One authoritative configuration for conditions, metrics, numerical tolerances and hard limits; evidence contract in verification.md §1 |

构建前一次性列出“指标→必要状态/参考/误差/需求与实际作用量→源端口与完整消费者→所在作用域→记录通道/名称/单位/时间阶段”，同时规划输出接口、临时或持久记录及初始化依赖。原生输出可用时复用，不默认新增大型透传Telemetry，不为布局删除真实输出；日志开关的配置和验证批次按真实作用域计入同一预算。可观测性与实际记录门禁见verification.md §1.1，不能用监测架构图代替实际状态核验。

Unspecified critical aircraft parameters are a blocker; do not fill them with arbitrary nominal values. Reference cases may suggest alternatives, not silently establish them.

## 2. Fidelity and information chain

- Use the least detailed model that answers the actual question; a linear longitudinal state-space LQR task does not require creating an unrelated nonlinear 6DOF vehicle.
- LQR and other state feedback designs must state whether `x` is directly provided by the simulator or obtained from measured/estimated variables. Do not mislabel perfect state feedback as implemented sensor/observer flight software.
- Include estimator/sensor dynamics only when supplied, required by the task, or necessary for a claimed implementation result. If ideal, label explicitly.
- Controller demands do not equal physical inputs. Quadrotor thrust/moment demands require configuration-aware allocation, feasible nonnegative thrust/speed and actuator dynamics/limits; fixed-wing surface/engine demands require trim bias, deflection/rate bounds and dynamics when modeled.
- Characterize theoretical control guarantees, simulation assumptions and actual tested envelope separately. In particular, local linear LQR guarantees and ideal sliding-mode arguments do not automatically cover large-angle nonlinear or sampled saturated operation.

### 2.1 按算法复杂度选择实现

简单误差、比例、线性组合优先Sum/Gain/Product；明确的标量代数可评估Fcn，但应核对其表达式限制、标量输出及工作区变量来源，不把Fcn当作矩阵计算器。矩阵状态反馈、混控、观测、调度或复杂分支主动比较MATLAB Function与原生矩阵模块；函数实现能改善接口契约、集中维护和复用时可采用，不强迫拆成大量算子，也不为展示功能人为增加复杂度。

函数边界固定输入输出维度、double/其他类型、参数来源、采样时间及状态语义；不依赖未声明基础工作区或隐藏persistent状态。连续积分、物理对象、执行机构、限幅和重要功能边界保留合适原生模块，不把完整模型无条件封装成函数。选择依据属于工程策略，不是MathWorks强制要求。算法独立数值验收按verification.md §1.2；编辑入口仍履行当前专业Skill/G1。

## 3. Physical and numerical basics

- Check exact native module semantics: whether force input already includes gravity; frame of inputs/outputs; port differences by MATLAB release; parameter units and indexing.
- Independently inspect quadrotor rotor lever arms and yaw reaction torques; don't carry over X allocation to + configuration. Use geometry `tau = r cross F` as an independent sign check when appropriate.
- A positive-down NED vertical coordinate is not altitude-above-origin; be explicit about any `h = -z_NED` relationship.
- For continuous plant + sampled loops, define periods, update ordering, hold/rate conversion, actuator lag and solver settings. Keep sample-start/midpoint/end/period-average signals distinct, with original timestamps and resampling method. Configuration is not proof of compiled rate or actual execution frequency; load runtime-diagnostics.md only when those require diagnosis. Numerical triggers/order are maintained in verification.md §3.
- Known-answer dynamics tests may use an analytical local equilibrium or controlled initial condition. Mission trim solves the user's target condition and validates internal states. Reuse applicable evidence; do not duplicate long simulations solely because both checks mention equilibrium.

## 4. Trim and control design

- Feasibility/actuator headroom before numerical solve; physically plausible guesses; state and derivative constraints; check solution branch and nonlinear residual; initialize motor/controller integrators and examine drift.
- PID: when cascade appropriate, establish inner loop first, then outer; test coupling, saturation and anti-windup.
- LQR: validate trim, A/B meanings, stabilizability, Q/R, feedback sign, actuator offset, local validity and nonlinear test where applicable. LQI另从稳态方程核对积分状态的可实现范围；权重归一化尺度不等于真实积分限幅，不以好看的瞬态掩盖不可达稳态。
- Sliding mode: validate sliding surface, equivalent/switching terms, reaching conditions, units, boundary layer, sampling, noise, and actuator constraints; no automatic guarantees beyond verified assumptions.
- Bounded tuning: define feasible parameter region, hard constraints, evaluation and hold-out scenarios, evaluation budget and stop rules; keep last *validated feasible* parameters. Failure is an acceptable result.
- 对约束分配/在线优化，分别验证静态可行、周期可达、实际执行机构传播及预测/实际作用量。求解退出状态、候选合法性、非线性接受准则与最终输出分别审查；无更新、合法回退与数值失败不是同一结果。
- 优化目标必须与正式指标建立对应；归一化总成本降低不保证单轴、力或力矩指标改善。力/力矩分别报告物理单位误差，不把量纲混合数值当统一物理范数。需要归因时才用固定输入、实际量级有限扰动和受控对照；局部敏感性不证明完整闭环因果或全局最优。

## 5. Reference cases

用户提供的课件、论文、开源项目或既有模型只作为有范围的参考，不建立其他构型的默认参数、混控、增益或有效包线。使用时记录来源、坐标、假设及未验证状态，独立核对公式/标注；没有提供这些资料也能按本文件的工程契约开展任务。

## 6. Personal diagram style and scoped delivery

### 6.1 五阶段语义布局与双路径

按“语义分组→模块/全局通道→连接表示→局部正交布线→适用验收”处理布局，不以逐线几何算法代替功能规划。构建前明确真实功能边界、主控制链、状态反馈、监测/记录接口及完整信号扇出；联合预留多端口尺寸、标签、引线和通道，不能先挤满画布再靠单块移动补救。只读任务止于规划，不因本节获得编辑/保存/编译/仿真权限；普通PID参数修改不触发布局、中文化或运行时监听。

**新建模型**：在获准的规格/架构阶段选择Direct、Goto/From、Bus或组合，冻结接口及预期源—消费者，不要求先建全直接线再转换。按真实功能建立顶层骨架与子系统，分批构建并与规格核对；不为缺失的旧模型制造基线，首个有效实现成为后续编辑检查点。架构授权须覆盖拟用表示，复用该授权，不逐标签重复申请。所选操作须由当前工具链实际支持；规划可行不等于构建、布局或功能已通过。

**既有模型表示改造**：先冻结受影响功能块身份、全部源/消费者/扇出、标签/Bus映射、参数/状态、类型/维度/单位/坐标/采样阶段、外部接口/日志及必要依赖；未知关键契约先补证据。选最小获准的表示差分，保留技术标识与执行语义。纯几何权限不包括新增路由块、端口或全图布局。 当前编辑器的自动布局若可能改变目标区外块位置或网络几何，且没有已验证的影响限制方式，禁止默认执行Goto/From或Bus转换。先保持现有表示，仅做已获准且可控的局部布局；确需转换时先识别工具的潜在影响域。只有影响能被可靠限制，或该已界定影响域事先获得明确的区域级授权，并具备相应即时、持久化和恢复验收能力，才允许执行。无法证明影响范围可控时返回BLOCKED，停在只读规划，不调用工具试错；局部几何操作本身不受控时也不得执行。不得事后扩大白名单、裸API补偿位置或以再编辑掩盖越界。

| 默认语义候选 | 组织规则 |
| --- | --- |
| 参考/任务指令 | 按控制层级靠近消费者，区分模式与连续目标 |
| 状态估计/反馈 | 外围反馈通道，区分真值/估计、坐标系及采样阶段 |
| 控制内部量 | 误差、积分、滤波、历史状态局部闭合 |
| 控制输出/分配 | 需求、静态可实现与动态实际力旋量分开 |
| 执行器命令/状态 | 分配与执行器相邻，命令不冒充实际反馈 |
| 动力学/环境 | 主链下游、扰动就近输入；力与力矩单位独立 |
| 遥测/诊断 | 按真实记录需求组织，不挤占主链；不补造不存在信号 |

同层相关接口相邻，同轴顺序一致不等于单位/维度相同。主链左到右、平行通道上下排列；反馈按真实端口从上方/下方外围返回，参考靠近控制器，分配与执行器相邻。不强制镜像、同向或不同信号共路；子系统按功能/行为/时序组织，不只为节省画布。不得默认创建纯透传Telemetry；有真实选择、计算、转换、打包或导出职责时才按需设置诊断模块。可在获准且工具支持时就源记录，但不得为美化删除输出、隐藏必要反馈或擅改已有接口。

### 6.1.1 连接表示与候选排序

| 表示 | 优先评估 | 必须检查 |
| --- | --- | --- |
| Direct | 主控制链、局部反馈及重要结构接口优先 | 全fanout、真实分支、端口对齐与可追踪 |
| Goto/From | 跨区长线、远距多消费者状态/参考、遥测 | Local默认，正确唯一源和完整消费者；短线不堆标签 |
| Bus | 共同语义、稳定接口或成组传递的状态/执行器/遥测 | 稳定元素名、类型/维度/单位/速率及消费映射；不是数值向量 |
| 保持原样 | 已清晰的既有模型默认保持；风险高、收益或能力不足亦保持 | 如实记录残留，不把无变化称优化通过 |

Goto/From和Bus是正常可评估的表示候选，不必先耗尽几何路由；但仍属结构编辑。采用MAB规范时固定版本/子条款及例外：na_0011-a要求Local，Scoped/Global须明确层级需求和批准的项目偏离，不能称该条款合规；适用b/c时核对Inport/Goto及From/Outport限制。jc_0171适用时保留结构子系统间真实显式关系，反馈双向可追踪，不加无用穿通或装饰线。产品支持不等于规范豁免。

Bus先按需求评估虚拟形式；非虚拟Bus、对象/端口或代码接口变化另查契约与授权，不为统一接口强制转型/重采样。标签可见域、非虚拟边界和元素访问必须解析验证。区分物理表示图与展开Goto/From、Bus后的逻辑图：获准表示改造允许白名单内物理变化，生产者—全部实际消费者及时间语义须等价；新建则与冻结规格比较。

先剔除授权、工具、语义/约束不合格的方案，再比较交叉、穿块/遮挡、无意义折返/绕行、关键路径查找、标签作用域复杂度、Bus维护量、遥测侵入和功能分区。优先Pareto支配及可解释取舍，不设置未经校准的固定权重；线长、折点或标签使用率不能单独判成功，取舍不清保持原样。

### 6.1.2 受控局部布线与能力边界

表示确定后先核对真实端口、双侧连接和完整邻区，再对齐模块并局部正交布线；不默认全图布局。不因方向不一致取消镜像；保留真实junction和fanout，不把几何拐点当语义节点。候选比较SID/类型/参数/接口及前后原生图，不把冲突转移至邻区。数值几何检查实际块矩形、端口、完整路径和约定的模型坐标净空；原生视觉独立检查线路、标签与文字遮挡及连接歧义，不把坐标净空冒称实际渲染宽度或未测字形包围盒。缺少必要证据的项目为UNVERIFIED，不能认证全图改善。

构建与布局阶段按实际功能作用域合并必要操作，子系统内部优先使用当前受控自动布局；顶层骨架的根级自动布局仅是候选结果，不保证实现规划的功能区。每次结构编辑后按实际影响核对功能分区和接口空间，记录请求与实际布局模式/范围；不以固定批数替代作用域分析。全部构建结束、接口和尺寸稳定后才冻结完整初始布局基线，不能将中间透传未连通状态当成功能完成。

结构完成后，只对已预检可行、影响边界可核验且获授权的对象进行有限Position整理；不以事后扩大白名单保持表面通过。出现大范围功能区混乱，或必须移动保护对象、反复补偿关联线路才能完成时，停止当前整理，报告架构/工具缺口；不继续坐标试摆，不依赖未经验证的复杂分支routeLine或Points精修完成交付。

`layout_mode="incremental"`不是块位置或邻区几何必然保持的保证。既有实验中Goto/From的逻辑等价不证明几何、编译、数值或保存重载通过；本布局升级的Bus改造仍为UNVERIFIED，直至独立实测。未验证状态不禁止有明确授权且安全边界可核验的新建构建/验证，但不得宣传为已通过能力。

能力仍为C0只读；C1仅已验证简单几何；C2指定线路原生路由须合规入口和范围证据；C3块布局须具体作用域授权；C4复杂分支精确重构未证实持久化/恢复前生产禁用；C5语义保持的表示改造需结构授权。C5不必然改变控制策略；新增延迟/速率转换、原子边界、控制结构或外部接口实质变化另评影响，不混入美化。表示工具与高级路由独立核查，路由实验失败不自动阻塞可单独验证的表示，但不得开放未通过路由。

按当前building-simulink-models读取→受控编辑（真实schema/layout_mode）→实际读取，partial立即停叠加。不得裸API、SLX/XML Points或未经许可的手工布局绕过编辑器。自定义路由需可审阅后端、严格校验、端点重解、会话/范围保护及重复请求锁，不能借其增删连接或自动注册；版本/网络/标签等超证据范围执行前拒绝。

局部候选最多两轮，合并已有初始整理/局部精修预算；复查不新增轮次，复查引发修改仍计预算。无新证据不重试。按[verification.md §8](verification.md#8-line-routing-persistence-and-file-recovery)激活适用的Q矩阵与V1/V2/V3/F1；纯几何不默认仿真，适用项缺证据不能记N/A逃避。中文显示与技术标识保护继续按§6.2。

规范来源按需核对：[na_0011](https://www.mathworks.com/help/releases/R2025a/simulink/mdl_gd/maab/na_0011scopeofgotoandfromblocks.html)、[jc_0171](https://www.mathworks.com/help/releases/R2025a/simulink/mdl_gd/maab/jc_0171clarificationofconnectionsbetweenstructuralsubsystems.html)、[Composite Interfaces](https://www.mathworks.com/help/releases/R2025a/simulink/ug/types-of-composite-interfaces.html)。一般理论/参数任务不因这些链接加载额外布局资料。


### 6.2 三级中文显示

| 层级 | 对象与动作 |
| --- | --- |
| 关键功能优先中文 | 控制器层级、分配、估计、执行机构、动力学、重要子系统/模式选择：提供准确简短的中文功能显示 |
| 特殊计算按需中文 | 补偿、预测、状态传播、非线性限制、动态反求等：只有语义不明或有阅读收益才说明，已有上下文清晰则省略 |
| 基础算子默认不注释 | Sum、Gain、Product、Integrator、Constant、Mux/Demux等保留简洁技术/数学表示；承担不明显的重要物理作用时按第二级例外处理 |

标注依据已有结构、参数和连接，不按英文名称猜功能。使用当前工具已核实支持的显示/注释方式；不支持时报告未完成，不能以擅自重命名替代。显示任务保留SID、Block Name、Signal Name、变量、路径、端口、参数、总线及脚本/代码生成接口，不把显示改动混同语义修改。只有另行明确授权实际重命名，且检查脚本/路径、测试、日志、接口及代码生成依赖并验证兼容后才做；禁止未经批准批量改名。

复用已有模块信息，批量处理已确认需要说明的关键功能，不逐基础块查询、翻译、注释或截图。只复查新增说明及相邻区域；遮挡时精简文字、局部调整，遵守上述有限轮次。参数修改不自动触发布局/中文化；标注数量或中文覆盖率不是完成指标。

### 6.3 交付

参数保持单一权威源，实验覆盖明确标识，不复制常量/增益到多个函数。仅交付适用且实际存在的模型、初始化/运行/设计脚本、配置、数据/指标、图、依赖版本及简短复现说明，不建空占位。实际编辑、编译、仿真、重试及wall按可取得证据记录；Token未由宿主提供则UNVERIFIED，不以字符数伪装Token。
