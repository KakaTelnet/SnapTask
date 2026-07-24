---
name: aim-review
description: Use when an aim document, project direction, or intent statement must be assessed before product planning or handoff.
---

# Aim Review

## Overview

Review the stated aim independently. Decide whether the background, target users, core value, boundaries, and success criteria are complete and consistent enough for downstream planning.

## Core Rule

Default to review-only behavior. Do not rewrite the aim, invent requirements, promote assumptions to facts, or change a verdict to satisfy pressure for approval.

## Review Workflow

1. Read the aim and any authorized context.
2. Separate stated facts, assumptions, unknowns, and missing information.
3. Read `references/aim-review-rubric.md`; apply every hard gate before scoring.
4. Choose exactly one result:
   - `通过: Approved`: ready for product planning.
   - `修订: Revision Required`: usable direction with correctable gaps.
   - `驳回: Rejected`: no usable direction or fundamental redefinition is required.
5. State each issue, its impact, and the decision or information required. Do not fill the gap for the author.
6. End with one concrete next action.

## Handoff Contract

- `通过: Approved`: hand the unchanged aim and review result to `$plan-make`.
- `修订: Revision Required`: return findings to `$aim-make` when available, or to the aim author.
- `驳回: Rejected`: stop planning and request a fundamentally redefined aim.
- Never upgrade a result during handoff or silently weaken boundaries, scope, or success criteria.

## Judgment Rules

- Reject an aim that states no concrete problem or opportunity.
- Reject an aim whose success criteria are purely subjective (feelings, opinions) with no observable anchor.
- Accept a tightly scoped aim where "nothing is excluded" only when the scope is genuinely atomic — a single, indivisible change.
- Treat vague user descriptions ("everyone", "better") as gaps requiring revision, not as approval blockers if the other dimensions are solid.
- Never approve when any hard gate is not satisfied, even if the score is high.

## Output Contract

Respond in the user's language and use this order. Preserve the three bilingual verdict labels exactly.

```text
审核结果: 通过: Approved | 修订: Revision Required | 驳回: Rejected
综合评分: N/10

总体判断:
<one concise paragraph>

做得好的地方:
- <evidence-based strength or "无">

关键检查:
| 检查项 | 结果 | 依据 |
| 背景 | 已满足 / 需要修订 / 暂无法判断 | ... |
| 目标用户 | 已满足 / 需要修订 / 暂无法判断 | ... |
| 核心价值 | 已满足 / 需要修订 / 暂无法判断 | ... |
| 边界 | 已满足 / 需要修订 / 暂无法判断 | ... |
| 成功标准 | 已满足 / 需要修订 / 暂无法判断 | ... |

需要改进的地方:
1. 问题:
   影响:
   修改要求:

下一步:
- <one action>
```

## Common Mistakes

- Rewriting by default instead of returning revision requirements.
- Treating confident language as evidence of clarity.
- Letting score arithmetic override a failed hard gate.
- Demanding product-plan detail from an aim document.
- Treating a missing user persona as a defect when the aim clearly targets a known system or team.
