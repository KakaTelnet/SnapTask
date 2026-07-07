---
name: kTask4AI
description: Guide a multi-turn decomposition conversation that turns broad software or product goals into AI-ready task cards with stable contracts, low conflict, and clear verification exits. Use when a user asks to split work, plan parallel AI agents, design task boundaries, coordinate multiple model changes, reduce merge conflicts, convert a broad requirement into task cards, or decide which parts must be serial versus parallel.
---

# kTask4AI

Use this skill to guide a conversation that turns a broad initiative into low-conflict, independently verifiable task units for AI agents. Do not split by human job titles first. Split by cognitive isolation, stable contracts, conflict radius, invariants, and verification exits.

## Core Rule

Prefer this framing:

```text
A good AI task is an independently understandable, independently changeable, independently verifiable, low-conflict cognitive unit.
```

Do not default to "frontend/backend/test/design" unless those boundaries also match low conflict and independent verification.

Do not produce final task cards until the target behavior, shared contracts, conflict boundaries, and verification exits are clear. If any of these are missing, run a clarification round first.

## Multi-turn Card Creation Protocol

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

## Workflow

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

## Conversation Modes

### Discovery Mode

Use when requirements are vague, contracts are unknown, or the project context has not been read. Output:

1. Restated target behavior
2. Known constraints
3. Assumptions
4. Up to 3 clarification questions
5. Local files or docs to inspect next, if available

### Draft Decomposition Mode

Use when enough context exists to propose task boundaries, but the user has not approved them yet. Output:

1. Overall decomposition judgment
2. Candidate contract tasks
3. Candidate journey or system-loop tasks
4. Candidate guard/check tasks
5. Parallel suitability and conflict risk for each candidate
6. Questions or choices that would change the split

Keep draft tasks short. Do not fill the full task-card template yet unless the user asks for final cards.

### Final Task Card Mode

Use after the user accepts the decomposition direction or explicitly asks for final cards. Output handoff-ready cards using `references/task-card.md`, followed by execution order and verification plan.

## Split Axes

Use these axes in preference order:

1. **Contract axis**: Split out anything that other tasks depend on.
2. **Journey axis**: Split by complete user/operator/system flow.
3. **Conflict axis**: Separate tasks by files and shared concepts they mutate.
4. **Invariant axis**: Separate rule-keeping checks from feature-building.
5. **Verification axis**: Separate work that requires different proof methods.
6. **Context-domain axis**: Keep each task centered on one business object, workflow, or subsystem.

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

## Output Shape

For normal requests with enough context, provide:

1. Overall decomposition judgment
2. Contract tasks
3. Parallel task candidates
4. Serial or blocking tasks
5. Invariant/guard tasks
6. Verification plan
7. Recommended execution order

For each task, use the task-card structure in `references/task-card.md` when the user needs an actionable handoff.

If the user asks to create cards over multiple rounds, follow the conversation modes instead of jumping directly to final cards.

## Quality Bar

Before finalizing, check every task card:

- Can another agent understand the task without hidden context?
- Does it say what files or domains are allowed and forbidden?
- Does it name dependent contracts and invariants?
- Does it have a real verification exit?
- Is its merge/conflict risk explicit?
- Is it small enough that success or failure is legible?
