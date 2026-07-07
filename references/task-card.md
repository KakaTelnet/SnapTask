# Task Card Reference

Use this template when producing handoff-ready task cards.

```text
Task id:
Task name:
Goal:
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

Field guidance:

- `Allowed changes` and `Forbidden changes` should be specific enough to stop accidental broad edits.
- `Inputs/assumptions` should capture unresolved facts the executing agent must verify or preserve.
- `Implementation notes` should guide direction without over-specifying code that the executing agent should discover locally.
- `Verification exit` must name concrete proof: tests, commands, API calls, screenshots, migrations, builds, or doc-code checks.
- `Handoff prompt` should be a concise prompt that can be copied directly to another AI agent.
