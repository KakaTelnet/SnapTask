---
name: snap-goal-review
description: Use when an AI-agent goal, project objective, success definition, investigation objective, or Goal draft must be assessed before planning, decomposition, execution, or handoff.
---

# Snap Goal Review

## Overview

Review the stated Goal independently. Decide whether an agent can know what done means, prove it, stay inside its authority, stop safely, and expose the remaining work.

## Core Rule

Default to review-only behavior. Do not rewrite the Goal, invent requirements, promote assumptions to facts, or change a verdict to satisfy pressure for approval. If the user explicitly asks for a reference revision, complete the independent review first and put the revision in a separate final section.

## Review Workflow

1. Read the Goal and only authorized context, sources, and evidence.
2. Separate stated facts, assumptions, unknowns, and missing evidence.
3. Read `references/review-rubric.md`; apply every hard gate before scoring.
4. Choose exactly one result:
   - `通过: Approved`: ready for planning or task decomposition.
   - `修订: Revision Required`: usable direction with correctable gaps.
   - `驳回: Rejected`: no usable completion basis or fundamental redefinition is required.
5. Map every acceptance condition to its required evidence.
6. State each issue, its impact, and the decision or information required. Do not fill the gap for the author.
7. End with one concrete next action.

## Handoff Contract

- `通过: Approved`: hand the unchanged Goal, review result, and evidence expectations to `$task-decompose`.
- `修订: Revision Required`: return findings to `$snap-goal-make` when available, or to the Goal author. Do not produce final task cards.
- `驳回: Rejected`: stop decomposition and request a fundamentally redefined Goal.
- Never upgrade a result during handoff or silently weaken acceptance, boundaries, constraints, evidence, or stop rules.

## Judgment Rules

- Reject an effort-only or action-only statement such as "try", "strive", "improve", "as appropriate", or "do our best" when it lacks a measurable end state.
- Accept a bounded investigation Goal without requiring a guaranteed discovery. It must define the inquiry boundary, deliverables, evidence, time or effort limit, and stop conditions.
- Treat implementation details as constraints only when they protect a real boundary or invariant. Flag Over-prescription when prescribed steps replace outcome judgment or unnecessarily remove execution autonomy.
- Require a one-to-one Acceptance-to-evidence map. Generic claims such as "test thoroughly" are not evidence plans.
- Require Source-of-truth priority and a conflict rule when multiple sources may disagree.
- Require Trade-off priority when cost, time, quality, scope, or safety limits can conflict.
- Count a no-progress rule only when it names a threshold and means no new evidence, no reduced blocker, and no reasonable alternative path.
- Never approve when any hard gate is not satisfied, even if the score is high.

## Output Contract

Respond in the user's language and use this order. Preserve the three bilingual verdict labels exactly; localize the other section headings when appropriate.

```text
审核结果: 通过: Approved | 修订: Revision Required | 驳回: Rejected
综合评分: N/12

总体判断:
<one concise paragraph>

做得好的地方:
- <evidence-based strength or "无">

关键检查:
| 检查项 | 结果 | 依据 |
| ... | 已满足 / 需要修订 / 暂无法判断 | ... |

Acceptance-to-evidence map:
| Acceptance | Required evidence | Mapping |
| ... | ... | Direct / Partial / Missing |

需要改进的地方:
1. 问题:
   影响:
   修改要求:

假设与未知项:
- <item or "无">

Remaining work and risks:
- Unfinished:
- Unverifiable:
- Blocked:
- Out of scope:
- Residual risks:

下一步:
- <one action>
```

For a draft Goal, the remaining-work section judges whether the Goal requires these categories to be exposed at completion; it does not claim execution has started. Never omit an unknown or remaining-work category that affects confidence.

## Common Mistakes

- Rewriting by default instead of returning revision requirements.
- Treating polished or confident language as evidence.
- Letting score arithmetic override a failed hard gate.
- Rejecting bounded research because its root cause cannot be guaranteed.
- Demanding implementation details instead of an observable result.
- Treating missing context as a defect without naming its impact and resolution.
