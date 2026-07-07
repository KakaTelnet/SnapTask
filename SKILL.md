---
name: kTask4AI
description: Guide a multi-turn decomposition and work-loop conversation that turns broad software or product goals into AI-ready task cards, dispatch plans, review checkpoints, follow-up cards, and integration decisions. Use when a user asks to split work, plan parallel AI agents, design task boundaries, coordinate multiple model changes, reduce merge conflicts, convert a broad requirement into task cards, track task-card progress, review completed agent work, or decide which parts must be serial versus parallel.
---

# kTask4AI

Use this skill to guide a conversation that turns a broad initiative into low-conflict, independently verifiable task units for AI agents, then keeps those cards useful through dispatch, review, integration, and follow-up loops. Do not split by human job titles first. Split by cognitive isolation, stable contracts, conflict radius, invariants, and verification exits.

## Core Rule

Prefer this framing:

```text
A good AI task is an independently understandable, independently changeable, independently verifiable, low-conflict cognitive unit.
```

Do not default to "frontend/backend/test/design" unless those boundaries also match low conflict and independent verification.

Do not produce final task cards until the target behavior, shared contracts, conflict boundaries, and verification exits are clear. If any of these are missing, run a clarification round first.

## Mode Selection

Choose the mode before choosing the output shape:

- **Discovery Mode**: requirements are vague, contracts are unknown, or local project context has not been read.
- **Draft Decomposition Mode**: enough context exists to propose task boundaries, but the user has not approved them.
- **Final Task Card Mode**: the user accepts the decomposition direction or explicitly asks for handoff-ready cards.
- **Work Loop Mode**: task cards already exist and the user wants to dispatch, track, review, integrate, revise, or close them.

If the user asks for "cards", "parallel agents", "dispatch prompts", or "handoff tasks" but the contracts or verification exits are still unclear, use Discovery or Draft Decomposition first and explain what must be clarified before final cards.

## Operating Protocol

When the user wants to create task cards through conversation:

1. Start with a short restatement of the target behavior.
2. Ask at most 3 high-leverage clarification questions per round.
3. After each round, summarize what is known, what is assumed, and what remains uncertain.
4. Do not ask about details that can be discovered from local files.
5. Prefer reading project context before asking implementation questions.
6. Identify shared contracts before proposing implementation tasks.
7. Produce a draft decomposition before producing full task cards.
8. Ask for confirmation before finalizing handoff-ready cards.

Ask questions only when the answer changes task boundaries, sequencing, contract shape, conflict risk, or verification. Otherwise make a reasonable assumption and label it.

## Decomposition Workflow

1. Read local project rules first when available: `AGENTS.md`, repo docs, architecture notes, and nearby module conventions. Treat them as constraints for all task cards.
2. State the target behavior in one sentence: what should change for a user, operator, or system.
3. Identify contracts before implementation tasks:
   - API request/response shapes
   - schemas, models, migrations, and durable data fields
   - state machines and status values
   - auth, permissions, visibility, and error semantics
   - routes, events, config names, and business terminology
4. Split by complete journeys or system loops, not by job role. A good journey has an actor, action, system response, persisted state, and observable result.
5. Check conflict radius. Tasks that touch the same shared files, state stores, schemas, migrations, or core components should be serialized or preceded by a contract task.
6. Extract invariants. Create explicit guard tasks when business rules, naming, privacy, permissions, or compatibility must remain true across multiple changes.
7. Assign verification exits. Every task needs a concrete way to prove completion: tests, API calls, page flows, builds, migrations, health checks, screenshots, or doc-code cross-checks.
8. Produce execution order:
   - contract-setting tasks first
   - high-conflict tasks serial
   - low-conflict journey tasks parallel
   - invariant and integration checks near the end

## Split Heuristics

Use these axes in preference order:

1. **Contract axis**: Split out anything that other tasks depend on.
2. **Journey axis**: Split by complete user/operator/system flow.
3. **Conflict axis**: Separate tasks by files and shared concepts they mutate.
4. **Invariant axis**: Separate rule-keeping checks from feature-building.
5. **Verification axis**: Separate work that requires different proof methods.
6. **Context-domain axis**: Keep each task centered on one business object, workflow, or subsystem.

Avoid cards that are only "implement backend", "build UI", "write tests", or "update docs". Those can be valid role lenses, but they are not good task boundaries unless they also match a stable contract, isolated journey, low conflict radius, and independent verification exit.

## Parallelization Rules

A task is usually safe to parallelize when:

- its file boundary is clear
- its contracts are already stable
- it does not need another task's intermediate output
- it has an independent verification exit
- failure does not corrupt shared data or invalidate other tasks
- the required context can be understood without loading the whole project

A task should be serial, or split again, when:

- it changes API, database, and multiple clients at once
- names or business concepts are still unsettled
- it touches shared state, shared components, or core config used by other tasks
- verification only works after a full system integration
- docs, code, and data disagree on the source of truth

## Role Perspective

Use role perspective to constrain execution and review criteria, not to choose the primary split. A role tells the agent how to judge tradeoffs and where not to wander; the task boundary still comes from contracts, journeys, conflict radius, invariants, and verification exits.

Prefer "role perspective + file boundary + acceptance standard" inside each task card. Example: "You are responsible for Web frontend experience. Modify only `web/`. Do not change `backend/`; write backend needs into the handoff notes."

## Output Shapes

### Discovery Mode Output

Use when requirements are vague, contracts are unknown, or local project context has not been read. Output:

1. Restated target behavior
2. Known constraints
3. Assumptions
4. Up to 3 clarification questions
5. Local files or docs to inspect next, if available

### Draft Decomposition Mode Output

Use when enough context exists to propose task boundaries, but the user has not approved them yet. Output:

1. Overall decomposition judgment
2. Candidate contract tasks
3. Candidate journey or system-loop tasks
4. Candidate guard/check tasks
5. Parallel suitability and conflict risk for each candidate
6. Questions or choices that would change the split

Keep draft tasks short. Do not fill the full task-card template yet unless the user asks for final cards.

### Final Task Card Mode Output

Use after the user accepts the decomposition direction or explicitly asks for final cards. Output handoff-ready cards using `references/task-card.md`, followed by execution order and verification plan.

Use the minimal task card when the user needs lightweight planning or a small number of handoff prompts. Use the full task card when the work is large, parallel, high-risk, or likely to return for review and integration.

### Work Loop Mode Output

Use after task cards have been created. Help the user dispatch, track, review, integrate, and revise task cards until the broader initiative is complete.

In Work Loop Mode, support these user intents:

1. **Dispatch**: choose the next ready card or batch, produce handoff prompts, and identify prerequisites.
2. **Status update**: mark cards as proposed, ready, in progress, blocked, done, needs revision, or superseded.
3. **Result review**: compare returned agent work against the card's goal, allowed changes, forbidden changes, invariants, and verification exit.
4. **Integration check**: identify contract drift, naming drift, shared-file conflicts, missing tests, and tasks that must be rerun or serialized.
5. **Follow-up generation**: turn new discoveries, bugs, missing docs, or scope changes into new task cards.
6. **Completion decision**: decide whether the overall initiative is ready for final verification, ship, archive, or another task-card round.

When reviewing completed work, do not accept "done" at face value. Require evidence that the verification exit was satisfied, or mark the card `Needs revision` with the smallest concrete next action.

Output:

1. Card status changes
2. Evidence reviewed
3. Gaps, risks, or contract drift
4. Next action per affected card
5. Updated execution order, if dependencies changed

## Task Statuses

Use these statuses consistently:

```text
Proposed: candidate card exists, but boundaries or contracts are not approved.
Ready: approved and unblocked; can be dispatched.
In progress: assigned to an agent or currently being executed.
Blocked: cannot proceed until a dependency, decision, credential, or contract is resolved.
Done: verification exit is satisfied and no blocking review issue remains.
Needs revision: returned work is incomplete, off-scope, unverified, or breaks an invariant.
Superseded: replaced by a newer card or no longer needed.
```

Every status update should include the reason and the next action.

## Example Split

Avoid splitting a billing upgrade project like this:

```text
1. Backend task
2. Frontend task
3. Test task
```

Prefer a contract-first, journey-centered split:

```text
1. Contract task: freeze plan, entitlement, billing status, and API semantics.
2. Journey task: user upgrades a plan and sees entitlement changes.
3. Journey task: failed payment enters retry state and shows recoverable UI.
4. Guard/check task: verify permissions, audit logging, rollback behavior, and docs-code consistency.
```

This keeps parallel work aligned around stable semantics instead of human job titles.

## Quality Bar

Before finalizing, check every task card:

- Can another agent understand the task without hidden context?
- Does it say what files or domains are allowed and forbidden?
- Does it name dependent contracts and invariants?
- Does it have a real verification exit?
- Is its merge/conflict risk explicit?
- Is it small enough that success or failure is legible?
