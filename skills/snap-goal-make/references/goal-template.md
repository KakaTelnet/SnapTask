# Goal Template

Use every section. Keep simple Goals compact. When a field does not apply, state why instead of omitting it.

Respond in the user's language. For Chinese output, localize the canonical headings exactly:

| English | Chinese |
| --- | --- |
| Goal Type | Goal 类型 |
| Background and Value | 背景与价值 |
| Goal | 目标 |
| Acceptance Criteria | 验收标准 |
| Completion Evidence | 完成证据 |
| Scope and Authority | 范围与权限 |
| Constraints and Priorities | 约束与优先级 |
| Sources of Truth | 事实来源 |
| Assumptions and Unknowns | 假设与未知项 |
| Stop and Escalation Conditions | 停止与升级条件 |
| Completion Report Requirements | 完成报告要求 |

## Outcome Goal

```text
Goal Type:
Outcome Goal

Background and Value:
<current state, affected actor or system, and value of completion>

Goal:
Move <target> from <current state> to <observable final state>.

Acceptance Criteria:
- AC-1: Under <condition>, <object> produces <observable result>.

Completion Evidence:
| Acceptance ID | Required evidence | Verification method |
| AC-1 | <artifact or observation> | <exact check> |

Scope and Authority:
- Included: <required work>
- Excluded: <non-goals>
- Allowed: <read or change boundary>
- Prohibited: <forbidden action>

Constraints and Priorities:
- Preserve: <invariant>
- Limits: <time, cost, calls, or not applicable with reason>
- Trade-off priority: <ordered priorities>

Sources of Truth:
- Authority: <code, document, API, or data>
- Conflict rule: <priority or not applicable with reason>

Assumptions and Unknowns:
- Assumptions: <explicit assumptions or none>
- Unknowns: <unknowns or none>

Stop and Escalation Conditions:
- Complete when every acceptance criterion has its required evidence.
- Stop after <N> attempts with no new evidence, no reduced blocker, and no reasonable alternative.
- Request confirmation before <risky, irreversible, external-impact, costly, or unauthorized action>.

Completion Report Requirements:
- Completed and evidence
- Unfinished
- Unverifiable
- Blocked
- Out of scope
- Residual risks
```

## Bounded Investigation Goal

```text
Goal Type:
Bounded Investigation Goal

Background and Value:
<observed issue and why the investigation matters>

Goal:
Within <time, cost, or attempt limit>, inspect <explicit boundary> and deliver <verified facts, excluded hypotheses, evidence-supported likely explanations, unknowns, and next actions>. Discovery of a root cause is not guaranteed.

Acceptance Criteria:
- AC-1: Every named source or path is inspected and recorded.
- AC-2: Every conclusion identifies its evidence and confidence.
- AC-3: Required deliverables distinguish facts, hypotheses, unknowns, and next actions.

Completion Evidence:
| Acceptance ID | Required evidence | Verification method |
| AC-1 | <inspection record> | <source, identifier, time, check, finding> |
| AC-2 | <evidence map> | <cross-check each conclusion> |
| AC-3 | <final investigation report> | <section completeness check> |

Scope and Authority:
- Included: <sources, systems, and time range>
- Excluded: <non-goals>
- Allowed: <normally read-only boundary>
- Prohibited: <writes or sensitive access not authorized>

Constraints and Priorities:
- Preserve: <safety, privacy, and production invariants>
- Limits: <time, cost, or attempt count>
- Trade-off priority: evidence quality and safety over explanation count or speed, unless the user decides otherwise.

Sources of Truth:
- Authority: <ordered sources>
- Conflict rule: <record and escalate unresolved conflict>

Assumptions and Unknowns:
- Assumptions: <explicit assumptions or none>
- Unknowns: <unknowns or none>

Stop and Escalation Conditions:
- Complete when the inquiry boundary and deliverables are exhausted, even if root cause remains unknown.
- Stop when the limit is reached or after <N> attempts with no new evidence, no reduced blocker, and no reasonable alternative.
- Request confirmation before sensitive access, writes, external impact, destructive action, or expansion beyond scope.

Completion Report Requirements:
- Completed inspections and evidence
- Unfinished
- Unverifiable
- Blocked
- Out of scope
- Residual risks
```

## Role Perspective

Include a role perspective only when it defines an allowed boundary, trade-off criterion, or review lens. Never add a ceremonial title. Put the resulting restriction in `Scope and Authority` or `Constraints and Priorities`.
