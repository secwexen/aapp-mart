# Commit Convention

AAPP-MART follows Conventional Commits to maintain consistent, readable, and traceable Git commit history.

## Format

`<type>(<scope>): <description>`

The scope is optional but recommended.

## Types

- `feat` - Introduce a new feature.
- `fix` - Fix a bug.
- `docs` - Documentation-only changes.
- `refactor` - Restructure code without changing external behavior.
- `test` - Add or update tests.
- `chore` - Maintenance tasks and auxiliary changes.
- `style` - Formatting and whitespace changes without affecting code behavior.
- `perf` - Improve performance.
- `build` - Change build system, packaging, or dependency configuration.
- `ci` - Modify CI/CD pipelines and automation workflows.

## Scope

The scope identifies the affected component or area of the codebase.

Common scopes include:

- `aapp`
- `mart`
- `engine`
- `runtime`
- `api`
- `cli`
- `contracts`
- `reporting`
- `config`
- `tests`
- `deps`
- `ci`
- `packaging`
- `core`

Scopes are not restricted to this list. Additional scopes may be introduced when necessary.

## Description Rules

- Use the imperative mood.
- Start with a lowercase letter.
- Keep descriptions concise and specific.
- Do not end the description with a period.
- Describe what the commit changes, not why it was requested.

## Examples

- `feat(aapp): add prediction confidence scoring`
- `feat(mart): add predefined attack scenarios`
- `feat(engine): integrate execution pipeline`
- `fix(runtime): handle failed execution lifecycle`
- `fix(api): validate execution requests`
- `docs(readme): update installation instructions`
- `refactor(contracts): simplify execution interfaces`
- `test(aapp): expand prediction scoring tests`
- `chore(deps): update project dependencies`
- `style(engine): fix code formatting`
- `perf(mart): optimize scenario processing`
- `build(packaging): update package configuration`
- `ci(github): add automated test workflow`

## Breaking Changes

Changes that introduce backward-incompatible behavior must be explicitly identified.

Use `!` after the type and optional scope:

`feat(api)!: change execution request format`

Alternatively, include a `BREAKING CHANGE:` footer describing the incompatibility.

Example:

`feat(contracts)!: update execution result structure`

`BREAKING CHANGE: Existing consumers must migrate to the new result structure.`
