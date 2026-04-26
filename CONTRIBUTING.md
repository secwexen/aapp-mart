# Contributing to AAPP-MART 

Thank you for your interest in contributing to AAPP-MART.  
We welcome contributions that improve code quality, security, and documentation.

## References

- [README.md](README.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [SECURITY.md](SECURITY.md)
- [LICENSE](LICENSE)
- [ROADMAP.md](ROADMAP.md)

## Getting Started

1. Fork the repository
2. Create a new branch from `main`
```bash
git checkout -b feature/your-feature-name
```

3. Set up a local development environment:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r dev-requirements.txt
```

If you are using VS Code, the recommended way is to open the project in the Dev Container environment.

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
  - For architectural proposals, please open a GitHub Discussion or an Issue with the label [design](https://github.com/secwexen/aapp-mart/issues?q=state%3Aopen%20label%3Adesign).
- Avoid introducing breaking changes without discussion.
- Keep code compatible with the project license (Apache-2.0 License).
  
## Branching and Merge Policy

- Use descriptive branch names: `feature/*`, `fix/*`, `docs/*`
- Base your branch on the latest `main`
- Before merging, rebase or squash commits to maintain a clean history
- Merges should be performed via Pull Request after review

## Release Workflow

- We follow **semantic versioning** (MAJOR.MINOR.PATCH).
- All releases must update the [CHANGELOG](CHANGELOG.md).
- Release candidates are tagged and tested before final publication.

## Commit Messages

- Use clear, descriptive commit messages
- Reference related issues when applicable
- Squash commits before submitting a pull request

See [COMMIT_CONVENTION.md](docs/COMMIT_CONVENTION.md) for full details.

## Pull Requests

All pull requests must:

- Be based on the latest `main` branch
- Pass all CI checks (unit tests, linting, formatting)
- Include a clear description of the changes
- Reference related issues or discussions when applicable
- Include necessary documentation updates if functionality or CLI changes

### Issue Labels

We use GitHub labels to guide contributors:
- `good first issue` → beginner-friendly tasks
- `help wanted` → tasks where community support is welcome

### Code Review Process

- At least one reviewer must approve the PR
- Reviewers check for code quality, tests, security, and documentation updates
- Feedback must be addressed before merging

## Documentation Contributions

- Contributions to the documentation are gladly accepted.
- Update [README.md](README.md) or other documentation as needed
- Follow Markdown formatting and style conventions

## Security and Ethics

AAPP-MART is a security-focused project.
Contributions must **not include exploit code**, malware, or content intended for illegal use.

- Contributions must remain within the scope of controlled, non-destructive security simulation.

Security issues should be reported according to the [SECURITY.md](SECURITY.md) policy.

## Code of Conduct

By participating in this project, you agree to act respectfully and professionally.
Harassment, abuse, or malicious contributions will not be tolerated.

## Thank You

Thank you for helping improve AAPP-MART!
