# Task Decompose Review 设计

## 背景与节奏判断

SnapTask 当前主链路为：

```text
snap-goal-make -> snap-goal-review -> task-decompose
```

Goal 生成与 Goal 审核已经形成独立生成、独立审核和自动化行为评估闭环；`task-decompose` 已有执行合同和任务卡模板，但尚无独立审核者，也没有专属行为 fixture 和端到端验证。新增 `task-decompose-review` 符合当前从 Goal 质量向任务拆分质量推进的整体节奏。

扩展后的主链路为：

```text
snap-goal-make
  -> snap-goal-review
  -> task-decompose
  -> task-decompose-review
```

实施顺序必须先稳定审核器，再验证生成器，最后连接端到端链路。不得同时修改生成合同和审核标准后直接用端到端结果证明二者正确。

## 目标

建立一个独立、只审核的 `task-decompose-review` Skill，并让它成为 SnapTask 自动化验证体系的一部分。

它接收以下原始材料：

1. Goal；
2. Goal Review 结果；
3. `task-decompose` 输出；
4. 用户明确提供的 bypass 或补充决定（如有）。

它判断 `task-decompose` 是否选择了正确模式、保留了上游合同、形成了低冲突且可验证的任务边界，并输出稳定、可由 harness 检查的审核结果。

## 非目标

- 不执行任务卡。
- 不修改项目代码或任务卡文件。
- 不默认重写拆分结果。
- 不替代 `snap-goal-review` 重新审核 Goal 本身。
- 不在首轮覆盖 Work Loop 的长期派发、跟踪和集成状态管理。
- 不先重构 Maker、Reviewer 和 Task Decompose 的现有 harness 为共享框架。

## Skill 结构

```text
skills/task-decompose-review/
├── SKILL.md
├── agents/openai.yaml
└── references/
    └── review-rubric.md
```

`SKILL.md` 保存审核协议、输入合同、模式判断和输出形状。`review-rubric.md` 保存硬门槛、评分维度、判定规则和典型失败模式。首轮不增加 README、安装文档或与执行无关的说明文件。

## 审核边界

`task-decompose-review` 检查以下硬门槛：

1. **上游门禁正确**：Approved、Revision Required、Rejected、Unreviewed Goal 分别进入正确的拆分模式；没有未经授权生成 Final Task Cards。
2. **验收覆盖完整**：Goal 的每个 acceptance condition 都映射到至少一个任务目标和具体 verification exit。
3. **合同保持完整**：范围、禁止事项、不变量、事实来源优先级、停止规则和人工升级条件没有被削弱或遗漏。
4. **任务边界独立**：每张任务卡可独立理解、修改和验证；拆分不是机械的前端、后端、测试角色切割。
5. **依赖顺序可执行**：共享合同先冻结，高冲突任务串行，满足条件的低冲突任务才并行。
6. **冲突风险明确**：共享文件、schema、状态、迁移、核心配置和集成风险均被标识。
7. **验证出口具体**：测试、命令、页面流程、API 调用或文档一致性检查具有可观察结果，不能只写“测试通过”或“确认正常”。
8. **完成可见性充分**：集成检查、残余风险、阻塞、未完成和下一步没有被隐藏。

任何硬门槛失败都不能被总分覆盖。

## Verdict 合同

首行必须使用以下一种结果：

```text
拆分审核结果: 通过: Approved
拆分审核结果: 修订: Revision Required
拆分审核结果: 驳回: Rejected
```

判定语义：

- `通过: Approved`：当前上下文中的拆分行为正确，所有硬门槛满足；对于 Revision Required、Rejected 或 Unreviewed Goal，正确停止、澄清或生成带标签草案也可以通过审核。
- `修订: Revision Required`：上游输入允许继续，但拆分结果存在可局部修复的覆盖、边界、依赖、冲突或验证缺口。
- `驳回: Rejected`：拆分绕过上游门禁、实质削弱 Goal、引入不安全权限，或输出与目标无关，不能通过局部修订成为可信任务集。

审核输出依次包含：综合评分、总体判断、做得好的地方、关键检查、Acceptance-to-task map、需要改进的地方、假设与未知项、剩余工作与风险、下一步。除非用户明确要求，审核器不输出完整重写版本。

## 自动化验证架构

### 第一层：静态合同

新增 Python 合同脚本，验证：

- 两个 Task Decompose Skill 的 frontmatter、关键协议和 Agent metadata；
- `task-card.md` 必需字段；
- Reviewer rubric 的硬门槛和判定规则；
- fixture manifest 的唯一 ID、状态分布、格式覆盖和输入完整性；
- live harness 的共识门禁和输出解析合同。

所有 Python 脚本放在 `tmp_py/`，通过项目 venv 执行。

### 第二层：受控 Reviewer fixture

建立 10 个 Goal Review + Task Decompose Output 配对样本，覆盖 Markdown、YAML、JSON 和文本格式。建议分布为 3 个 Approved、5 个 Revision Required、2 个 Rejected。

案例至少覆盖：

1. 合格的 contract-first 拆分；
2. 非 Approved Goal 的正确停止或草案处理；
3. acceptance condition 未映射；
4. 不安全并行和共享文件冲突；
5. 范围、禁止事项或不变量被遗漏；
6. verification exit 主观或不可执行；
7. 按前后端角色机械切分；
8. 缺少集成检查和残余风险；
9. 绕过上游审核门禁；
10. 实质削弱安全或事实来源约束。

Reviewer live eval 在隔离上下文中只读取 `task-decompose-review` 及其直接引用，不读取无关仓库材料。

### 第三层：端到端 live eval

端到端评估分两次独立模型调用：

1. `task-decompose` 根据 Goal 和 Goal Review 生成结果；
2. 新鲜上下文中的 `task-decompose-review` 审核原始输入与生成结果。

首批只选代表性场景：Approved Goal、Revision Required Goal、Rejected Goal、Unreviewed Goal。先小范围运行，健康后再扩展全量。fixture live eval 默认运行 3 次，每个 case 以至少 2 次通过作为共识门禁，同时保留每次原始输出和失败原因。

## Harness 边界

首轮采用独立 harness，不抽取跨 Skill 共享框架。每个 harness 至少支持：

- `--list`：只加载案例，不调用模型；
- `--ids`：选择代表性案例；
- `--repeat`：显式覆盖运行次数；
- 默认 fixture 运行 3 次；
- run-level 和 case-level 共识汇总；
- 原始模型输出写入 `/private/tmp`，不污染仓库。

模型退出失败、首行 verdict 不匹配、必需语义段缺失或出现未授权重写都计为该次运行失败。只有 case-level 共识通过才返回成功退出码。

## TDD 与 Skill 验证顺序

1. 先写静态合同和受控失败案例，确认 RED 来自缺少新 Skill 或缺少必需行为。
2. 初始化 `task-decompose-review` Skill 骨架。
3. 写最小审核合同和 rubric，使静态合同 GREEN。
4. 先运行无新审核 Skill 的行为基线，记录自然失败或错误判定。
5. 使用新 Skill 运行同一批样本，修复实际暴露的合同缺口。
6. 小范围 live eval 健康后，再运行 3 次共识全量 Reviewer fixture。
7. Reviewer 自身稳定后，最后运行端到端生成与审核链路。

## 完成标准

- 新 Skill 目录通过官方 Skill 快速校验。
- 静态合同、fixture loader、自测、JSON/YAML 解析和 `git diff --check` 全部通过。
- 10 个受控 Reviewer fixture 达到 case-level 共识门禁。
- 4 个代表性端到端场景正确处理上游状态并由独立审核者通过。
- 现有 Maker 和 Goal Reviewer 合同保持通过。
- 未修改 Work Loop 长期状态协议，也未进行跨 harness 重构。

## 风险与控制

- **审核器与生成器相互迁就**：用人工标注的受控 fixture 先稳定审核器，再做端到端。
- **双模型随机性叠加**：保留原始输出，分层报告生成失败和审核失败，使用 2/3 共识而非单次 verdict。
- **Verdict 语义混淆**：固定使用“拆分审核结果”首行，同时把 Goal Review 结果保留为输入证据。
- **Skill 体积膨胀**：核心协议放 `SKILL.md`，详细评分和失败模式放单层 reference。
- **范围扩张到执行编排**：首轮明确排除 Work Loop 长期状态管理和实际任务执行。
