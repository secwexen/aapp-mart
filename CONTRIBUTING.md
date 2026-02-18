# Contributing to AAPP-MART

> Note: AAPP-MART is currently under active development.  
> Core components may evolve as the architecture stabilizes.  

Thank you for your interest in contributing to AAPP-MART. We welcome contributions that improve code quality, security, and documentation.  

---

## Getting Started

1. Fork the repository
2. Create a new branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Set up a local development environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

---

## Development Guidelines

- Follow Python best practices (PEP 8).
- Write clear, readable, and well-documented code.
- Add or update tests for new functionality.
- Use the provided test framework (pytest) and ensure all tests pass:

  ```bash
  pytest tests/
  ```

- All new features must align with the documented architecture.
- Architectural changes require prior discussion.
- Avoid introducing breaking changes without discussion.
- Keep code compatible with the project license (Apache-2.0 License).

---

## Branching and Merge Policy

- Use descriptive branch names: `feature/*`, `fix/*`, `docs/*`
- Base your branch on the latest `main`
- Before merging, rebase or squash commits to maintain a clean history
- Merges should be performed via Pull Request after review

---

## Commit Messages

- Use clear, descriptive commit messages
- Reference related issues when applicable
- Squash commits before submitting a pull request

---

## Pull Requests

All pull requests must:

- Be based on the latest `main` branch
- Pass all CI checks (unit tests, linting, formatting)
- Include a clear description of the changes
- Reference related issues or discussions when applicable
- Include necessary documentation updates if functionality or CLI changes

### Code Review Process

- At least one reviewer must approve the PR
- Reviewers check for code quality, tests, security, and documentation updates
- Feedback must be addressed before merging

---

## Documentation Contributions

- Contributions to the documentation are gladly accepted.
- Update [README.md](README.md) or other documentation as needed
- Follow Markdown formatting and style conventions

---

## Security and Ethics

AAPP-MART is a security-focused project.
Contributions must **not include exploit code**, malware, or content intended for illegal use.

- Contributions must remain within the scope of controlled, non-destructive security simulation.

Security issues should be reported according to the [SECURITY.md](SECURITY.md) policy.

---

## Code of Conduct

By participating in this project, you agree to act respectfully and professionally.
Harassment, abuse, or malicious contributions will not be tolerated.

---

# Thank You

Thank you for helping improve AAPP-MART!
