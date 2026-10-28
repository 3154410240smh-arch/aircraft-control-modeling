# Toolchain capability and specialist routing

仅在能力发现、版本或连接问题时加载；保留文件名以保持引用兼容，不携带某台机器的状态保证。先看当前工具schema和所需专业Skill；复用版本/接口未变的证据，不全量探测、不自动安装或修改配置。

## 1. Relevant specialist routing

从当前客户端提供的技能目录/资源和工具清单发现能力；下表名称仅是检索线索，不保证安装、版本或接口可用。只加载任务所需组合，缺失时说明受影响步骤。

| 任务 | 按需专业Skill |
| --- | --- |
| 结构/参数/连接编辑 | building-simulink-models |
| 当前模型/选中对象 | simulink-interactions |
| SimulationInput/Output仿真 | simulating-simulink-models |
| 持久化模型测试 | testing-simulink-models |
| 配平/线性化 | simulink-linearize |
| 对象/算法规格 | specifying-plant-models / specifying-mbd-algorithms |
| 函数错误/函数耗时 | matlab-debugging / matlab-optimize-performance |
| 已定位的块方法异常 | simulink-debug-commandline |
| 模型整体耗时/求解器问题 | 对应Simulink Profiler技能 |
| 工程依赖/自定义库 | managing-simulink-projects / setup-custom-libraries |

这不是默认加载清单。并行仿真、故障、安全、代码生成仅在任务需要且获准时另行发现相关Skill。

## 2. Check the current contract, not a remembered version

- 编辑前核对当前building-simulink-models规定的读取/编辑/核查顺序、布局参数、partial处理及禁止的原始API。参数如layout_mode以真实schema为准；不得凭历史版本补造字段、可选工具或例外。布局调用的请求模式、实际自动执行范围和是否可抑制须分别取证；未核实前不得假定存在块锁定、排除区域或指定线路几何保持能力，也不猜造禁用自动布局字段。
- 库配置/策略批准及规格Skill的中间审查是独立门禁；普通建模不自动触发，不手写配置绕过。发现具体延迟/反馈要求与物理语义冲突时，提窄范围决定，不盲加延迟或秘密忽略规则。
- 工具别名以会话schema解析，MCP模型工具不一定是普通MATLAB函数；which为空不证明工具缺失。反之文件存在不证明函数可解析。原生类型/对象、端口和测试夹具契约均需匹配实际版本，不把某类Chart检查器用于不同对象并声称已验证。
- 分清注册、连接、函数解析、目标会话、读取、编译和实际运行。只读请求可能触发编译、回调、缓存或工作区改变，先核对真实副作用及授权；工具发现不授权初始化共享会话、修改MATLAB路径或启动服务。

## 3. Minimal capability evidence and bounded recovery

仅核对本次所需连接、版本、原生模块语义、许可证或编译器；记录来源、版本、模式和适用范围。安装/license test不等于运行或部署成功，历史成功不保证当前环境。无目标机测试则实时能力UNVERIFIED。

接口故障先用现有信息区分连接、schema、会话、解析/依赖或模型错误，最小补查须获授权；没有改变前提不重复失败调用。缺工具只阻断相关阶段。若必须安装、升级、配置路径/服务或更改专业Skills，列具体操作、影响与恢复方案申请授权；不以普通MATLAB代码或直接工程文件修改绕过必需编辑器。当前客户端无安全能力时报告限制，不把建议描述为已实现。


## 4. Optional controlled routing extension

指定线路路由需要独立核实的受控入口，model_edit通用params字典不证明任意几何操作可用。MCP自定义扩展支持情况按当前版本官方契约确认；若仅支持基本标量参数，复杂请求可用JSON字符串承载，但后端仍须严格校验结构、类型、范围、端点与预算，禁止任意代码。唯一工具/函数名、独立扩展，不修改或遮蔽官方model_edit，不自动修改持久配置或MATLAB路径。

注册、函数解析、真实执行、即时保护、保存重载、原生视觉和文件恢复是不同能力。隔离注册成功不证明模型操作；简单无分支成功不开放复杂分支。未经验证的复杂分支routeLine及Points精修继续禁用，不能作为架构交付依赖；不以属性可写、函数返回成功或单例Position通过推定这些能力已具备。失败/超时先查原请求记录，不以新request_id绕过锁存继续编辑。新增工具的实际版本、适用限制和测试证据放工程能力记录，不把某台机器的路径、工具名和发布状态写成通用保证。

## 5. Signal representation edits (conditional)

仅在拟新增/改造Direct、Goto/From、Bus或接口时核对：当前受控编辑器是否支持所需原生块/端口、参数、作用域与即时读取；标签源/可见域、Bus元素及边界能否可靠解析，必要编译能否在授权会话取得类型/维度/采样证据。操作字段、端口和库路径以当前schema/安装版本为准，不在此固化假想操作。新建可按已批准架构直接构建表示；既有先冻结原信号契约，不能因工具缺字段改用裸API。

通用params或工具已注册不证明标签/Bus等价，也不证明任意几何能力。表示改造与高级routeLine能力独立，后者仍需§4门禁。缺少关键解析/作用域保护或恢复能力时阻断该操作，保留可做的只读规划；不自动安装/初始化/注册、修改官方SATK或生产配置。普通参数/理论任务不触发这份检查。

既有模型改造还须查清编辑器自动布局的实际影响域，以及是否存在经过验证的位置/邻区限制方式。不得把incremental、通用params、工具注册或逻辑连接保持当作范围保护保证；缺少可界定的影响边界，或缺少该范围的可靠限制/事前区域授权及验收能力时，仅保留规划并返回BLOCKED，不试错、不修改官方工具。当前布局升级的Bus执行验证尚未完成；新建直接按表示规划也须在当前支持接口内实际验证，不外推为全工作流PASS。

## 6. Signal logging configuration (conditional)

仅在需要时序证据或修改日志时加载。本次LQR-PD案例中，connect携带DataLogging="on"虽返回ok，实际源输出端口仍off；随后signal configure使用实际连接ID、params.DataLogging="on"，分作用域调用后七路实际on并取得时序。这证明该案例/当时版本的configure路径，不证明所有connect都不支持，也不证明其他模型、覆盖配置或持久化已通过。能力缓存记录工具版本、请求与实际结果，变化后只复验受影响前提。

按当前schema使用真实信号目标，每次model_edit只允许一个作用域；根级子系统命名接口从实际model_read获取，不把新建ref的数字端口别名机械用于已有连接，不凭CONNECTION_NOT_FOUND重新接线。configure为参数修改，显式layout_mode但不推定自动布局必然跳过或几何保持。DataLogging字段及其对象归属以当前工具与实际源端口查询为准；通用params字典不保证所有嵌套字段生效。

每批按专业Skill核对实际结构/状态，并确认所需源端口或已验证有效覆盖配置的记录开关、名称、抽取/点数限制及保护对象；model_read未暴露的记录字段需获准的只读查询补齐，可合并同检查点读取。partial立即读取，未生效、区外变化或状态不明则停后续编辑/仿真；不重连、不改SLX、不以未经授权的直接set_param端口或其他写入绕过G1，也不因工具失败自动获准替代方法。入口缺失或剩余额度不足则BLOCKED。观测与输出门禁只在verification.md §1.1维护，不在此复制整套验收。


## 7. MATLAB Function / Fcn（条件触发）

先核查当前专业Skill和真实接口。model_edit创建块及外部结构、连线；MATLAB Function对应Stateflow.EMChart，不与Stateflow.Chart内的EMFunction混淆。仅当当前专业Skill明确允许且本次模型编辑已获授权时，使用其规定的Stateflow API配置函数内部Script、数据契约和更新方式；此例外不允许原始API替代普通结构或几何编辑。不能从通用configure字典推定Script受支持，也不能凭模型名猜完整路径；从实际SID解析，编辑后实际读取及编译。Fcn表达式只用已核实的合法Expr，不推断其支持矩阵或任意MATLAB函数。

函数选型和数值测试见engineering.md §2.1与verification.md §1.2。本规则不授予安装、初始化、修改工具或生产配置权限；实际能力和局限保存在项目证据中，不将单例结果推广到其他版本/模型。

MATLAB Function编译可能产生JIT/代码生成缓存。首次编译前读取实际pwd及有效CacheFolder/CodeGenFolder，按规范化真实路径确认位于本次获准项目/恢复目录；优先使用工具已支持的项目工作目录参数，不改生产MCP配置或全局缓存配置。若默认输出跟随pwd，实际读取验证该关系；不能假定脚本run返回后仍在项目目录。发现区外生成文件先保留身份与哈希，再在授权保护/恢复范围内处理，不混入正式安装目录。

项目取证脚本须依赖闭合：没有对话框参数的原生块可以合法返回空DialogParameters，不能假定一律为struct，也不能静默忽略非空未知类型。不要把工具扩展初始目录下的私有包当作项目隐含依赖；改变工作目录后若解析失败，先停止该辅助步骤，使用已审查的项目内只读I/O，不擅自addpath或修改工具配置。
