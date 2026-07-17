# Repository Guidelines

## Project Structure & Module Organization

SnapTask is a Codex plugin composed of three cooperating skills:

- `skills/snap-goal-make/` turns rough intent into a complete Goal through guided conversation.
- `skills/snap-goal-review/` independently checks Goal quality and returns a verdict.
- `skills/task-decompose/` converts approved Goals into verifiable task cards.

Each skill keeps its executable contract in `SKILL.md`, launcher metadata in `agents/openai.yaml`, and supporting templates or rubrics in `references/`. Plugin metadata lives in `.codex-plugin/plugin.json`. Durable behavior cases are stored in `tests/*.json`; Python contract and evaluation harnesses live in `tmp_py/`. Design and implementation notes belong in `ai_docs/notes/`.

## Build, Test, and Development Commands

There is no compilation step. Use the project virtual environment for Python checks:

```bash
./venv/bin/python3 tmp_py/tmp_20260715_goal_make_contract.py
./venv/bin/python3 tmp_py/tmp_20260715_goal_review_contract.py
./venv/bin/python3 tmp_py/tmp_20260715_run_goal_make_evals.py --self-test
./venv/bin/python3 tmp_py/tmp_20260715_run_goal_review_evals.py --fixtures --list
jq empty .codex-plugin/plugin.json tests/goal-make-cases.json tests/goal-review-cases.json
git diff --check
```

Run `--validate-existing` on the Maker harness to recheck retained behavior outputs without invoking a model. The Reviewer contract also validates the indexed multi-format corpus in `tests/goal-fixtures.json`; pass `--fixtures` to the Reviewer evaluation harness only when live behavioral evidence must be refreshed.

## Coding Style & Naming Conventions

Write concise, imperative Markdown. State boundaries, required behavior, and output shapes explicitly. Keep skill directories and front-matter names in lowercase kebab-case; preserve established snake_case YAML keys such as `display_name` and `default_prompt`. Use ASCII punctuation unless localized content requires otherwise. Keep references inside the owning skill instead of creating cross-skill hidden dependencies.

## Testing Guidelines

Treat JSON cases as durable regression contracts. Every new behavior needs a focused case with required, forbidden, or structured assertions. Keep Maker creation separate from Reviewer scoring, preserve approved Goals unchanged, and map revisions back to `$snap-goal-make`. Before submitting, run both contract scripts, relevant harness checks, JSON validation, and `git diff --check`.

## Commit & Pull Request Guidelines

Use short imperative subjects matching repository history, for example `Refine Goal maker behavior fixtures`. Keep commits scoped to one protocol or validation change. Pull requests should summarize behavior changes, list affected skills, include exact validation commands and results, link related issues, and call out contract or handoff changes. Screenshots are needed only for user-visible rendered UI changes.
