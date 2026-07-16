# Repository Guidelines

## Project Structure & Module Organization

This repository contains a collection of composable Codex skills for defining, reviewing, and decomposing AI-agent work.

- `skills/snap-goal-make/` contains the guided Goal generator.
- `skills/task-decompose/` contains the task decomposition and work-loop skill.
- `skills/snap-goal-review/` contains the independent Goal quality reviewer.
- `.codex-plugin/plugin.json` exposes the collection as the `snaptask` Codex plugin.
- Each skill owns its `SKILL.md`, optional `agents/openai.yaml`, and supporting `references/` files.

Keep skill-specific reference material under that skill's `references/`. Add agent configuration under that skill's `agents/` only when it is specific to a supported agent surface.

## Build, Test, and Development Commands

There is no build step for this repository. Validate changes with lightweight checks:

- `rg --files` lists the complete tracked content shape.
- `sed -n '1,220p' skills/task-decompose/SKILL.md` reviews the decomposition workflow.
- `sed -n '1,220p' skills/task-decompose/references/task-card.md` reviews the handoff template.
- `sed -n '1,220p' skills/snap-goal-review/SKILL.md` reviews the Goal reviewer.
- `sed -n '1,260p' skills/snap-goal-make/SKILL.md` reviews the multi-turn Goal creation workflow.
- `sed -n '1,260p' skills/snap-goal-make/references/goal-template.md` reviews the canonical Goal forms.
- `python3 tmp_py/tmp_20260715_goal_make_contract.py` checks the Maker contract and fixture coverage.
- `python3 /path/to/plugin-creator/scripts/validate_plugin.py .` validates plugin discovery metadata.

If you add generated validation scripts, place temporary scripts in `tmp_py/` and keep them out of the skill runtime unless they become intentionally maintained tooling.

## Coding Style & Naming Conventions

Use concise Markdown with clear headings and actionable bullets. Keep skill instructions imperative and specific: say what the agent should do, when to do it, and what output shape is expected.

Use lowercase kebab-case for skill and directory names, such as `ai-task-decomposition`. YAML keys should remain snake_case where already established, for example `display_name` and `default_prompt`.

Prefer ASCII punctuation in repository files unless a file already uses non-ASCII content for a clear reason.

## Testing Guidelines

No automated test framework is configured. Before submitting changes, manually verify that:

- Every `skills/*/SKILL.md` front matter includes valid `name` and `description` fields.
- Each skill directory matches its front matter `name`.
- Relative links and file references point to existing files within the owning skill.
- Any task-card changes preserve all fields needed for handoff-ready work.
- Goal Maker never scores or emits a review verdict as its own judgment.
- Confirmed Goal drafts hand off to `$snap-goal-review`; approved Goals hand off unchanged to `$task-decompose`.
- `tests/goal-make-cases.json` retains all required Discovery, Draft, Revision, Rejected, Approved, and bypass scenarios.

## Commit & Pull Request Guidelines

Use simple imperative commit messages, such as `Add Goal review rubric`.

Pull requests should include a short summary, the files changed, and a note on manual validation performed. Link related issues when available. Screenshots are usually unnecessary unless a tool renders this skill in a UI and the display text changes.

## Agent-Specific Instructions

When updating these skills, preserve the decomposition skill's core framing: tasks should be independently understandable, changeable, verifiable, and low-conflict. Avoid broad role-based splits unless they also match stable contracts and isolated verification exits.
