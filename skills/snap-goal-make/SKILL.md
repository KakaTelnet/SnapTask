---
name: snap-goal-make
description: Use when a rough intention, project objective, investigation idea, or existing Goal draft must be turned into a complete AI-agent Goal through context-aware multi-turn conversation before independent review.
---

# Snap Goal Make

## Overview

Turn rough intent into a complete Goal through progressive conversation. Support general AI-agent work and read authorized project rules, code, interfaces, tests, and documentation when the Goal concerns software.

## Core Boundary

Create and revise Goals; do not judge their quality. `$snap-goal-review` is the sole quality judge.

- Do not score the Goal or apply the Reviewer's hard gates as an internal review.
- Do not emit `通过: Approved`, `修订: Revision Required`, or `驳回: Rejected` as your own verdict.
- Do not invent requirements, silently resolve source conflicts, or turn a recommendation into a confirmed user decision.
- Do not use patch-based revision, Goal version numbers, or hidden persistent workflow state.
- After Review returns Approved, preserve the complete Goal unchanged.
- Do not create, require, or simulate a programmatic JSON review return.
- Consume snap-goal-review's existing human-readable contract.
- Before confirmation or review, record every normative user decision in the complete Goal. A normative decision is any decision affecting outcome, acceptance, evidence, scope or authority, constraints or priorities, source priority or conflict handling, assumptions or unknowns, or stop or escalation behavior.

## Entry Selection

Choose the entry from the user's current input:

- Rough intent: start with Intake and Discovery.
- Existing Goal draft: preserve usable content and ask only about decisions that materially affect the Goal.
- Review report: follow Result Handling.
- Approved Goal: hand the unchanged Goal to `$task-decompose` with the review result and evidence expectations.

If the request contains several independent initiatives, propose Goal boundaries first and ask the user to choose one. Do not draft one Goal that hides several independent outcomes.

## Authorized Context

1. Identify what sources the user supplied or authorized.
2. For software work, read nearby `AGENTS.md`, relevant code, interfaces, tests, and project documentation before asking questions those files can answer.
3. Treat discovered facts as context, not as user preference.
4. When sources conflict, state each source and conflict, then ask for a priority or escalation rule.
5. When access fails, name the unavailable source and continue only with explicit unknowns.
6. Do not inspect unrelated files merely to fill every template field.

## Goal Type

Choose one drafting form from `references/goal-template.md`:

- Outcome Goal: an observable final state can be defined.
- Bounded Investigation Goal: discovery cannot be guaranteed, but inquiry boundary, deliverables, evidence, limits, and stopping point can be defined.

Never rewrite an uncertain investigation as a promise to find a root cause.

## Multi-Turn Protocol

### Intake

Restate the intended change or inquiry in one sentence. Identify authorized sources and whether the request is one Goal or several independent Goals.

### Discovery

Resolve one primary decision per turn. Ask only when the answer changes the outcome, acceptance, evidence, scope, authority, invariant, priority, source rule, or stop condition.

- Read authorized context instead of asking the user for discoverable facts.
- Ask the user about consequential preferences and decisions.
- Make a low-risk assumption only when it does not change a critical decision; label it explicitly.
- When the user asks you to decide a consequential preference, propose a recommendation and wait for confirmation.

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

End with one primary question. Do not print the complete Goal on every turn.

### Draft

When the consequential decisions are resolved, generate one complete Goal using every heading in `references/goal-template.md`. Keep the length proportional to risk and complexity. Explain why a field is not applicable instead of omitting it.

- Respond in the user's language and apply the exact localized heading and Goal type value maps from the template.
- Number acceptance criteria `AC-1`, `AC-2`, and so on.
- Map every acceptance ID to concrete evidence and a verification method.
- Include source priority or explain why conflict handling is not applicable.
- Include a precise no-progress rule and human escalation triggers.
- Require the completion report to expose Completed, Unfinished, Unverifiable, Blocked, Out of scope, and Residual risks.
- Include a role perspective only when it constrains authority, trade-offs, or review criteria.
- Put every normative user decision in the complete Goal; do not leave one only in conversation context, a summary, or a handoff.

Label the output `Goal Draft` and ask the user to confirm it before review. If the user explicitly skips review, label it `Unreviewed Draft`; do not claim it is execution-ready and do not proactively hand it to task decomposition. An explicit bypass is handled by `$task-decompose` under its own rules.

## Review Handoff

After user confirmation, hand the complete Goal unchanged to `$snap-goal-review`. The handoff contains only:

1. The confirmed complete Goal.
2. Authorized source provenance or access needed to inspect sources referenced by that Goal.

The complete Goal is the sole normative contract. Do not include hidden decisions, summary-only rules, persuasion, a desired score, or a requested verdict. Reviewer and Task Decompose must be able to act from the Goal and authorized source provenance alone. If `$snap-goal-review` is unavailable, return the complete Goal plus an exact prompt telling the user to review it with `$snap-goal-review`; never simulate the verdict.

## Result Handling

Consume the Reviewer's existing result without changing its meaning:

- `通过: Approved`: preserve the complete Goal unchanged and hand it, the review result, and evidence expectations to `$task-decompose`.
- `修订: Revision Required`: use each finding's Problem, Impact, and Revision requirement to ask only for affected decisions. Then regenerate the complete Goal, show it in full, and request user confirmation before another complete review.
- `驳回: Rejected`: preserve valid background facts, return to defining the outcome or bounded inquiry, and do not cosmetically rewrite the rejected statement.

If the same unresolved issue returns twice without new information, pause and ask the user for the missing decision. Never lower acceptance, evidence, boundaries, safety, or stop rules merely to obtain approval.

## Output Shapes

### Discovery

```text
目标理解 / Goal understanding:
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

### Goal Draft

Use the complete selected form from `references/goal-template.md`, then ask for confirmation. Do not append a score or review verdict.

### Revision

```text
本轮处理的 Reviewer 反馈:
- <problem and required decision>

<the complete regenerated Goal>

请确认这份完整 Goal 是否可以重新交给 $snap-goal-review。
```

### Approved Handoff

```text
<the unchanged approved Goal>

审核结果与证据要求:
<the Reviewer result>

下一步:
- 交给 $task-decompose。
```

## Common Mistakes

- Rebuilding the Reviewer inside Maker.
- Dumping the full template before consequential decisions are known.
- Asking for facts available in authorized local files.
- Treating current implementation as the user's desired final state.
- Hiding an unresolved source conflict inside an assumption.
- Editing only one field after review instead of regenerating the complete Goal.
- Adding a role title that changes no boundary or evaluation criterion.
