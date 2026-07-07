# Task Card Reference

Use the minimal template for lightweight planning, small tasks, or quick dispatch prompts. Use the full template for large, parallel, high-risk, or review-heavy work.

## Minimal Task Card

```text
Task id:
Task name:
Status:
Goal:
Scope:
Forbidden changes:
Dependent contracts:
Invariants to preserve:
Verification exit:
Conflict risk:
Parallel suitability:
Handoff prompt:
Next action:
```

## Full Task Card

```text
Task id:
Task name:
Status:
Owner/agent:
Goal:
Role perspective:
User/system outcome:
Context domain:
Allowed changes:
Forbidden changes:
Inputs/assumptions:
Dependent contracts:
Invariants to preserve:
Implementation notes:
Verification exit:
Conflict risk:
Parallel suitability:
Prerequisites:
Handoff prompt:
Result summary:
Verification evidence:
Review notes:
Next action:
Follow-up tasks:
```

Use these suitability labels:

```text
Contract task: freezes request/response shapes, schemas, statuses, permissions, names, or other shared semantics before dependent work starts.
Parallel-safe: contract is stable, files are isolated, verification is independent.
Parallel-with-contract: can run after a contract task lands or is explicitly frozen.
Serial: shared state, shared files, migrations, or unsettled semantics make parallel work risky.
Guard/check: does not primarily build; verifies invariants, docs, compatibility, or integration.
```

Use these status labels:

```text
Proposed: candidate card exists, but boundaries or contracts are not approved.
Ready: approved and unblocked; can be dispatched.
In progress: assigned to an agent or currently being executed.
Blocked: cannot proceed until a dependency, decision, credential, or contract is resolved.
Done: verification exit is satisfied and no blocking review issue remains.
Needs revision: returned work is incomplete, off-scope, unverified, or breaks an invariant.
Superseded: replaced by a newer card or no longer needed.
```

Field guidance:

- `Status` should always include a reason when reported in prose.
- `Owner/agent` may be a named agent, model, worktree, thread, or "unassigned".
- `Role perspective` should constrain judgment and review criteria, not replace task boundaries.
- `Allowed changes` and `Forbidden changes` should be specific enough to stop accidental broad edits.
- `Inputs/assumptions` should capture unresolved facts the executing agent must verify or preserve.
- `Implementation notes` should guide direction without over-specifying code that the executing agent should discover locally.
- `Verification exit` must name concrete proof: tests, commands, API calls, screenshots, migrations, builds, or doc-code checks.
- `Handoff prompt` should be a concise prompt that can be copied directly to another AI agent.
- `Result summary` should be filled only after work returns; keep it factual and brief.
- `Verification evidence` should cite exact commands, outputs, screenshots, URLs, commit ids, or files reviewed.
- `Review notes` should capture off-scope changes, invariant breaks, contract drift, and residual risk.
- `Next action` should say dispatch, revise, integrate, verify, wait, split, supersede, or close.
