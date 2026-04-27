# Conventional Commit Template

## Format

`<type>(<scope>): <description>`

## Types

- feat     - A new feature  
- fix      - A bug fix  
- docs     - Documentation changes only  
- refactor - Code change that neither fixes a bug nor adds a feature  
- test     - Adding or updating tests  
- chore    - Build process or auxiliary tool changes  
- style    - Formatting, whitespace, etc. (no code logic change)

## Scope (optional)

- Indicates the part of the codebase affected (e.g. auth, api, ui, database, config)

## Examples

- feat(auth): add login with email and password  
- fix(api): handle null response in user service  
- docs(readme): update installation instructions  
- refactor(payment): simplify transaction logic  
- test(auth): add unit tests for login service  
- chore(deps): update dependencies  
- style(ui): fix indentation in header component
