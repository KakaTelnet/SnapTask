---
name: aim-make
description: Use when rough intent, a project idea, or an existing aim draft must be clarified into a complete aim document (where to go) through multi-turn conversation before independent review.
---

# Aim Make

## Overview

Turn rough intent into a complete aim document (`aim.md`) through progressive conversation. Clarify background, target users, core value, explicit boundaries, and success criteria.

## Core Boundary

Create and revise aim documents; do not judge their quality. `$aim-review` is the sole quality judge.

- Do not score the aim or apply the Reviewer's rubric as an internal review.
- Do not emit `通过: Approved`, `修订: Revision Required`, or `驳回: Rejected` as your own verdict.
- Do not invent requirements or silently resolve conflicts between user statements.
- After Review returns Approved, preserve the complete aim unchanged.
- Before confirmation or review, record every normative user decision in the complete aim.

## Entry Selection

Choose the entry from the user's current input:

- Rough intent: start with Intake and Discovery.
- Existing aim draft: preserve usable content and ask only about decisions that materially affect the aim.
- Review report: follow Result Handling.
- Approved aim: hand the unchanged aim to `$plan-make` with the review result.

If the request contains several independent initiatives, propose aim boundaries first and ask the user to choose one.

## Multi-Turn Protocol

### Intake

Restate the intended direction in one sentence. Identify whether the request is one aim or several independent aims.

### Discovery

Resolve one primary decision per turn. Ask only when the answer changes one of the five aim dimensions:

- **背景**: problem, current state, or opportunity
- **目标用户**: who benefits, who is affected
- **核心价值**: why this matters, what changes
- **不做的事**: what is explicitly out of scope
- **成功标准**: observable condition for "done"

Make a low-risk assumption only when it does not change a critical decision; label it explicitly.

### Progressive Summary

During Discovery, keep the response compact:

```text
已确认 / Confirmed:
- <confirmed facts and decisions>

暂定假设 / Tentative assumptions:
- <labeled low-risk assumption or none>

待确认 / Open decision:
- <the one decision that blocks useful progress>
```

End with one primary question. Do not print the complete aim on every turn.

### Draft

When the five dimensions are sufficiently resolved, generate one complete aim using every section in `references/aim-template.md`. Explain why a field is not applicable instead of omitting it.

- Respond in the user's language.
- Put every normative user decision in the complete aim.
- Label the output `Aim Draft` and ask the user to confirm it before review.

## Review Handoff

After user confirmation, hand the complete aim unchanged to `$aim-review`. The handoff contains only:

1. The confirmed complete aim.
2. Any context the user authorized for clarifying the aim.

The complete aim is the sole normative contract. Do not include hidden decisions, summary-only rules, persuasion, a desired score, or a requested verdict.

## Result Handling

Consume the Reviewer's existing result without changing its meaning:

- `通过: Approved`: preserve the complete aim unchanged and hand it, the review result, to `$plan-make`.
- `修订: Revision Required`: use each finding to ask only for affected decisions. Then regenerate the complete aim, show it in full, and request user confirmation before another complete review.
- `驳回: Rejected`: preserve valid background facts, return to defining the aim, and do not cosmetically rewrite the rejected statement.

If the same unresolved issue returns twice without new information, pause and ask the user for the missing decision.

## Output Shapes

### Discovery

```text
方向理解 / Direction understanding:
<one sentence>

已确认 / Confirmed:
- ...

暂定假设 / Tentative assumptions:
- ...

待确认 / Open decision:
- ...

问题 / Question:
<one primary question>
```

### Aim Draft

Use the complete form from `references/aim-template.md`, then ask for confirmation. Do not append a score or review verdict.

### Revision

```text
本轮处理的 Reviewer 反馈:
- <problem and required decision>

<the complete regenerated aim>

请确认这份完整 Aim 是否可以重新交给 $aim-review。
```

### Approved Handoff

```text
<the unchanged approved aim>

审核结果:
<the Reviewer result>

下一步:
- 交给 $plan-make。
```

## Common Mistakes

- Rebuilding the Reviewer inside Maker.
- Dumping the full template before the five dimensions are known.
- Treating a vague wish as a confirmed direction.
- Hiding an unresolved conflict inside an assumption.
- Editing only one field after review instead of regenerating the complete aim.
