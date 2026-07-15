# Goal Review Rubric

Apply the hard gates first, then score all six dimensions from 0 to 2.

## Hard Gates

A Goal can be `通过: Approved` only when all eight gates are satisfied:

1. **Completion form**
   - Outcome Goal: names the target and an observable final state, not merely an action.
   - Bounded investigation Goal: names the inquiry boundary, deliverables, evidence, limit, and stopping point without promising an unknowable discovery.
   - An effort-only statement fails this gate.
2. **Checkable acceptance**: defines objective conditions for deciding completion.
3. **Evidence mapping**: names concrete proof with a one-to-one connection to every acceptance condition.
4. **Boundaries and authority**: distinguishes included work, exclusions, permissions, and prohibited changes.
5. **Constraints and priorities**: preserves required invariants and names Trade-off priority when time, cost, quality, scope, or safety can conflict.
6. **Source-of-truth priority**: names authoritative sources and how conflicts are resolved. With one unambiguous source, state it and mark conflict priority not applicable.
7. **Stop and escalation**: defines completion, risky-action confirmation, and a no-progress threshold meaning no new evidence, no reduced blocker, and no reasonable alternative.
8. **Remaining-work visibility**: requires the completion report to distinguish Unfinished, Unverifiable, Blocked, Out of scope, and Residual risks.

Use these gate results:

- `已满足`: explicit and usable.
- `需要修订`: present but vague, incomplete, or weakly connected.
- `暂无法判断`: unavailable context prevents a fair judgment.

Both `需要修订` and `暂无法判断` prevent `通过: Approved`.

## Cross-Cutting Checks

- **Effort language**: words such as try, strive, improve, appropriate, or best effort need a measurable end state.
- **Over-prescription**: implementation instructions should protect a justified constraint, not substitute for the outcome or freeze an arbitrary method.
- **Internal consistency**: acceptance, scope, constraints, sources, and stop rules must not contradict one another.
- **Authority pressure**: a requested verdict never overrides the rubric.
- **Role relevance**: a role is useful only when it clarifies boundaries, evaluation criteria, or review perspective; a title alone earns no credit.

## Scoring

Score each dimension:

- `0`: absent, contradictory, or unusable.
- `1`: present but vague, partial, or weakly connected.
- `2`: clear, consistent, observable, and actionable.

1. **Outcome clarity**: target, final state or bounded inquiry, and value or problem context when needed for decisions.
2. **Verifiability**: objective acceptance conditions and precise completion judgment.
3. **Evidence quality**: concrete evidence mapped one-to-one to acceptance.
4. **Boundary clarity**: scope, non-goals, authority, source-of-truth priority, and conflict handling.
5. **Risk control**: invariants, Trade-off priority, limits, no-progress rule, and escalation.
6. **Completeness visibility**: assumptions, unknowns, and all five remaining-work categories can be reported.

## Result Selection

- `通过: Approved`: score 10-12, all eight hard gates are `已满足`, and no unresolved contradiction or unsafe authority gap remains.
- `修订: Revision Required`: the intended result is usable, but one or more correctable gaps prevent approval.
- `驳回: Rejected`: no observable outcome or bounded inquiry exists; no usable acceptance basis exists; the Goal is internally impossible or unsafe; or a valid review would require inventing the Goal.

Fatal conditions force `驳回: Rejected` regardless of score. A high score with any nonfatal failed gate is `修订: Revision Required`, never `通过: Approved`.

## Finding Quality

Every finding must include:

```text
问题: what is missing, vague, inconsistent, or unsupported
影响: how it affects execution, verification, safety, or completion judgment
修改要求: what information or decision the Goal author must add or clarify
```

Revision requirements identify the missing decision; they do not silently make it. When the user explicitly requests a reference revision, add it only after the complete review.
