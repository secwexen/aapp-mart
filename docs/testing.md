# AAPP-MART Testing & Quality Assurance

This document outlines testing procedures, quality checks, and best practices for contributing to the AAPP-MART project.

---

## 1. Unit Testing

Unit tests ensure individual modules behave as expected. All new features or bug fixes **must** include corresponding tests.

### Run All Unit Tests

```bash
pytest
```

> Make sure all tests pass before submitting code or pull requests.

### Test Coverage

Verify that your changes are sufficiently covered:

```bash
coverage run -m pytest
coverage report
```

Aim for high coverage, especially for core logic like AAPP prediction and MART agent behavior.

---

## 2. Linting & Code Style

Maintain code consistency with PEP8 and project conventions.

### Using Makefile 

```bash
make lint
```

### Directly with Pylint

```bash
pylint src/aapp_mart
```

Linting ensures readability, maintainability, and reduces errors.

---

## 3. Integration Testing

Integration tests validate interactions between:

- **AAPP** (Attack Path Predictor)
- **MART** (Multi-Agent Red Team)
- **CORE** (Simulation Brain / Orchestrator)

Check that:

- AAPP correctly generates attack paths
- MART agents execute safely without destructive payloads
- CORE orchestrates simulations consistently and maintains the Knowledge Graph state

---

## 4. Deterministic Replay

AAPP-MART simulations are deterministic when input data and configuration remain identical.

- Use the same target dataset and environment configuration
- Verify that repeated runs produce the same output
- Ensure reports and risk scores are consistent

---

## 5. Test Data & Examples

Sample datasets for testing are included in:

```
src/aapp_mart/data/
examples/
```

Use these datasets for both unit and integration tests.

> Note: Some modules are under active development; tests may be skipped or marked as expected failures until features are implemented.

---

## 6. Continuous Integration (CI)

- GitHub Actions workflows are configured for testing and CodeQL analysis
- All pull requests must pass CI checks before merging

> CI ensures code quality and early detection of potential errors.

---

## 7. Contributing Guidelines for Testing

1. Write tests for any new feature or bug fix
2. Use existing test framework (pytest)
3. Run all tests locally before pushing changes
4. Ensure code style checks pass
5. Document any new test cases or mock datasets

---

## 8. Security Considerations

Testing must never involve:

- Destructive payload execution
- Unauthorized scanning or exploitation
- Any actions outside controlled or lab environments

Follow responsible testing practices and only use explicitly authorized targets.
