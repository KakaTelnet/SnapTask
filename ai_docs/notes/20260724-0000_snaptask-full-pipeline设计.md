# SnapTask 完整 Pipeline 设计

**日期：2026-07-24**
**状态：设计完成，待实施**

---

## 1. 概述

SnapTask 从现有的 4 阶段模块层 pipeline（Goal → Review → Decompose → Review）扩展为覆盖项目全生命周期的双层架构：

- **项目层**：5 对 skill，产出 5 份结构化文档，覆盖从意图到模块拆分的完整规划
- **模块层**：现有 4 阶段 pipeline，每个模块独立执行
- **反馈闭环**：实现中发现的问题通过 `$issue` 机制回溯到上游文档

### 核心原则

- 每个 Maker skill 只负责产出，不评判质量
- 每个 Reviewer skill 独立评判，返回三态裁决：通过 / 修订 / 驳回
- 文档是唯一真相源（Single Source of Truth）
- 上游文档变更自动触发下游 stale 标记
- 下游实现反馈通过 $issue 上报，不自动阻塞管道
- 任何 skill 不得静默削弱上游 skill 的产出

---

## 2. 文档体系

### 2.1 文档分层

用户项目中的存放位置：`项目根目录/docs/.snaptask/`

```
docs/.snaptask/
  aim.md              # L0 意图 — where to go
  plan.md             # L1 产品设计 — how to do
  spec.md             # L2 架构设计 — what to do
  rules.md            # L3 规则 — task rules
  tasks.md            # L4 模块拆分总表 — task models
  adr/                # 重要架构决策记录
  modules/            # L4 各模块详细设计
    <module-name>.md
```

### 2.2 文档依赖关系

```
aim.md  →  plan.md  →  spec.md  →  rules.md
                                    ↓
                                tasks.md
                                    ↓
                              modules/*.md
```

### 2.3 文档契约

#### aim.md（where to go）

| 章节 | 内容 |
|------|------|
| 背景 | 一句话描述现状和问题 |
| 目标用户 | 谁会用到这个产品/项目 |
| 核心价值 | 解决什么问题、为什么值得做 |
| 不做的事 | 明确边界，防止范围蔓延 |
| 成功标准 | 怎么判断「做成了」 |

#### plan.md（how to do）

| 章节 | 内容 |
|------|------|
| 功能清单 | 按优先级排列的功能列表（P0/P1/P2） |
| 非功能需求 | 性能、安全、可用性、可维护性约束 |
| 用户旅程 | 核心路径的端到端描述 |
| 阶段划分 | 里程碑和每个阶段交付什么 |
| 风险记录 | 已知风险、假设、待确认点 |

#### spec.md（what to do）

| 章节 | 内容 |
|------|------|
| 总体架构 | 系统分层、技术选型、关键决策（链接 ADR） |
| 模块清单 | 每个模块的：职责一句话、对外接口、依赖的模块 |
| 数据模型 | 核心实体、关系、约束 |
| 接口约定 | 模块间 API 契约（输入/输出/错误） |
| 部署视图 | 运行时的拓扑（如果适用） |

#### rules.md（task rules）

| 章节 | 内容 |
|------|------|
| 项目结构 | 目录布局、文件命名 |
| 代码规范 | 语言、格式、lint 规则 |
| 测试要求 | 测试框架、覆盖率底线、运行命令 |
| 工作流程 | 分支策略、commit 规范、PR 流程 |
| 业务约束 | 非技术的硬性限制（合规、性能上限等） |

#### tasks.md（task models）

| 章节 | 内容 |
|------|------|
| 模块列表 | 每个模块的名称和一句话职责 |
| 依赖关系 | 模块间的构建顺序（DAG） |
| 每个模块的验收标准 | 独立可验证的「完成」定义 |
| handoff 链接 | 每个模块到 `goal-make` 的入口引用 |
| 待解决 issue | 来自实现反馈的 issue 列表 |

---

## 3. Skill 架构

### 3.1 Skill 清单（7 对，14 个）

| 层 | Maker | Reviewer | 含义 | 产出 |
|----|-------|----------|------|------|
| 项目层 | `aim-make` | `aim-review` | where to go | `aim.md` |
| 项目层 | `plan-make` | `plan-review` | how to do | `plan.md` |
| 项目层 | `spec-make` | `spec-review` | what to do | `spec.md` + `adr/` |
| 项目层 | `rules-make` | `rules-review` | task rules | `rules.md` |
| 项目层 | `tasks-make` | `tasks-review` | task models | `tasks.md` + `modules/*.md` |
| 模块层 | `goal-make` | `goal-review` | 已有：模块入口 | Goal |
| 模块层 | `task-decompose` | `task-decompose-review` | 已有：任务拆分 | Task Cards |

### 3.2 Skill 存放位置

```
skills/
  aim-make/              # 新增
  aim-review/            # 新增
  plan-make/             # 新增
  plan-review/           # 新增
  spec-make/             # 新增
  spec-review/           # 新增
  rules-make/            # 新增
  rules-review/          # 新增
  tasks-make/            # 新增
  tasks-review/          # 新增
  snap-goal-make/        # 已有（后续可重命名为 goal-make）
  snap-goal-review/      # 已有（后续可重命名为 goal-review）
  task-decompose/        # 已有
  task-decompose-review/ # 已有
```

### 3.3 Skill 命名规范

- Maker：`<what>-make`
- Reviewer：`<what>-review`
- 纯小写英文单词，连字符分隔
- 不使用前缀

---

## 4. Pipeline 流程

### 4.1 完整链路

```
aim-make
  ↓  handoff: $aim
aim-review ──── 修订 → 回 aim-make
  ↓ 通过              驳回 → 停止
plan-make
  ↓  handoff: $plan
plan-review ─── 修订 → 回 plan-make
  ↓ 通过              驳回 → 停止
spec-make
  ↓  handoff: $spec
spec-review ─── 修订 → 回 spec-make
  ↓ 通过              驳回 → 停止
rules-make
  ↓  handoff: $rules
rules-review ── 修订 → 回 rules-make
  ↓ 通过              驳回 → 停止
tasks-make
  ↓  handoff: $tasks
tasks-review ── 修订 → 回 tasks-make
  ↓ 通过              驳回 → 停止
          ↓
    对每个模块（按依赖顺序）:
    goal-make → goal-review → task-decompose → task-decompose-review
          ↓
    实现中发现问题 → $issue 反馈
```

### 4.2 Reviewer 三态裁决

与现有 `snap-goal-review` 一致：

| 裁决 | 含义 | 后果 |
|------|------|------|
| 通过 | 文档完整、一致、可进入下一阶段 | 自动 handoff 到下游 maker |
| 修订 | 有缺陷但可修复 | 返回 maker 修改，修改后重新经过本 gate |
| 驳回 | 根本性问题，不可修 | 管道停止，需要人工介入 |

### 4.3 不变式

- 任何 skill 不得静默削弱上游 skill 的产出
- 通过状态必须原封不动地保留到下游 handoff
- 驳回的文档不得进入下游

---

## 5. 变更传播机制

### 5.1 Stale 标记

当上游文档被修改时，所有直接和间接依赖它的下游文档自动标记 `stale`。

**传播规则：**

```
aim.md 变更
  → plan.md    标记 stale
  → spec.md    标记 stale
  → rules.md   标记 stale
  → tasks.md   标记 stale

plan.md 变更
  → spec.md    标记 stale
  → rules.md   标记 stale
  → tasks.md   标记 stale

spec.md 变更
  → rules.md   标记 stale
  → tasks.md   标记 stale

rules.md 变更
  → tasks.md   标记 stale
```

**Stale 检测时机：** 每个 reviewer 在审查前先检查当前 skill 依赖的上游文档是否 stale。如果有 stale 标记，直接返回「修订」，要求先跑上游 skill 更新。

### 5.2 与 Needs-Review 的区别

| 标记 | 含义 | 触发源 |
|------|------|--------|
| `stale` | 上游文档被修改，下游必须重做 | 文档变更 |
| `needs-review` | 下游实现反馈了问题，需要评估 | `$issue` 上报 |

`needs-review` 不自动阻塞管道，由 reviewer 评估后决定是否升级。

---

## 6. 反馈闭环：$issue 机制

### 6.1 触发条件

Agent 在实现阶段（模块层 task-decompose 的 Work Loop 或实际编码时）发现上游文档有问题。

### 6.2 $issue 结构

```
$issue
  source: <哪个 task / 模块>
  layer:  aim | plan | spec | rules | tasks
  severity: block | warn
  what: <具体什么问题>
  suggest: <建议怎么改>
```

### 6.3 Severity 两态

| 级别 | 含义 | 处理方式 |
|------|------|----------|
| `block` | 阻塞当前模块，不改无法继续 | 对应文档 revoke 通过状态 → 下游 stale → 管道暂停 |
| `warn` | 可继续，但应在下次迭代修复 | 记录到文档的「待解决 issue」章节 → 管道继续 |

### 6.4 回溯路径

```
实现中发现问题
  → 生成 $issue
  → issue 按 layer 路由到对应上游文档
  → 对应文档标记 needs-review
  → 对应 review skill 评估 issue
      ├─ block → 文档 revoke 通过状态 → 下游全部 stale → 管道暂停
      └─ warn  → 记录到文档 → 管道继续
```

---

## 7. 模块层并行

### 7.1 模块依赖 DAG

`tasks.md` 中定义模块间的依赖关系。没有依赖的模块可并行进入模块层 pipeline。有依赖的模块必须等上游模块完成后再启动。

### 7.2 模块层 pipeline 复用

每个模块独立走完整的 4 阶段：

```
goal-make → goal-review → task-decompose → task-decompose-review
```

模块层 skill 的行为不变，只是入口从对话变成了 `$tasks` handoff 引用。

---

## 8. Handoff 引用规范

### 8.1 引用列表

| 引用名 | 指向 | 产出者 |
|--------|------|--------|
| `$aim` | `aim.md` 内容 | `aim-review` 通过 |
| `$plan` | `plan.md` 内容 | `plan-review` 通过 |
| `$spec` | `spec.md` 内容 | `spec-review` 通过 |
| `$rules` | `rules.md` 内容 | `rules-review` 通过 |
| `$tasks` | `tasks.md` 内容 + `modules/*.md` | `tasks-review` 通过 |
| `$goal` | 单个模块的 Goal | `goal-review` 通过（已有） |
| `$issue` | 实现反馈问题 | 模块层 agent 发现时 |

### 8.2 引用规则

- 下游 maker 通过 handoff 引用读取上游文档，不直接读文件
- 引用内容为 reviewer 通过时的快照，不可被下游篡改
- 文档修改后，旧引用失效，必须重新经过 reviewer 生成新引用

---

## 9. 与现有系统的关系

### 9.1 现有 skill 保留

- `snap-goal-make` / `snap-goal-review`：保留，作为模块层入口。后续考虑重命名为 `goal-make` / `goal-review`
- `task-decompose` / `task-decompose-review`：保留，不变

### 9.2 新增 5 对 skill

全部为项目层 skill，独立开发，不修改现有 skill 行为。

### 9.3 测试体系复用

- 每个新 skill 照现有模式建立 JSON 回归契约（`tests/`）
- 每个新 skill 照现有模式建立 structural contract 脚本（`tmp_py/`）
- Reviewer skill 使用 fixture 机制（`tests/<name>-fixtures/`）
- 适用时使用 E2E 评估（生成 → 审查）

---

## 10. 实施优先级

| 优先级 | Skill 对 | 理由 |
|--------|----------|------|
| P0 | `aim-make` / `aim-review` | 入口，无它后续无法开始 |
| P0 | `tasks-make` / `tasks-review` | 连接项目层和模块层的关键节点 |
| P1 | `plan-make` / `plan-review` | aim 之后自然下一步 |
| P1 | `spec-make` / `spec-review` | 架构设计，决定模块边界 |
| P2 | `rules-make` / `rules-review` | 规则可先硬编码，后用 skill 替代 |
| P2 | `$issue` 反馈闭环 | 需要先有实现经验才能验证反馈机制 |
