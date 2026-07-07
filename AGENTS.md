# Repository Guidelines

## Project Structure & Module Organization

This repository contains a Codex skill for decomposing large work into AI-friendly task units.

- `SKILL.md` is the primary skill definition, including metadata, workflow, output shape, and quality bar.
- `agents/openai.yaml` defines the agent-facing display name, short description, and default prompt.
- `references/task-card.md` contains the reusable task-card template and suitability labels.

Keep new persistent reference material under `references/`. Add new agent configuration files under `agents/` only when they are specific to a supported agent surface.

## Build, Test, and Development Commands

There is no build step for this repository. Validate changes with lightweight checks:

- `rg --files` lists the complete tracked content shape.
- `sed -n '1,220p' SKILL.md` reviews the main skill text.
- `sed -n '1,220p' references/task-card.md` reviews the handoff template.

If you add generated validation scripts, place temporary scripts in `tmp_py/` and keep them out of the skill runtime unless they become intentionally maintained tooling.

## Coding Style & Naming Conventions

Use concise Markdown with clear headings and actionable bullets. Keep skill instructions imperative and specific: say what the agent should do, when to do it, and what output shape is expected.

Use lowercase kebab-case for skill and directory names, such as `ai-task-decomposition`. YAML keys should remain snake_case where already established, for example `display_name` and `default_prompt`.

Prefer ASCII punctuation in repository files unless a file already uses non-ASCII content for a clear reason.

## Testing Guidelines

No automated test framework is configured. Before submitting changes, manually verify that:

- `SKILL.md` front matter includes valid `name` and `description` fields.
- Relative links and file references, such as `references/task-card.md`, point to existing files.
- Any task-card changes preserve all fields needed for handoff-ready work.

## Commit & Pull Request Guidelines

This checkout does not include Git history, so follow simple imperative commit messages, such as `Clarify task-card verification guidance`.

Pull requests should include a short summary, the files changed, and a note on manual validation performed. Link related issues when available. Screenshots are usually unnecessary unless a tool renders this skill in a UI and the display text changes.

## Agent-Specific Instructions

When updating this skill, preserve its core framing: tasks should be independently understandable, changeable, verifiable, and low-conflict. Avoid broad role-based splits unless they also match stable contracts and isolated verification exits.
