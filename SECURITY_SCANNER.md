# AAPP-MART Security Scanning Guide

This document describes the security scanning standards used in the AAPP-MART project.

---

## 1. Static Code Analysis

We use **Bandit**, **Flake8**, **Black**, and **isort** through pre-commit hooks.

Run manually:
```
bandit -c bandit.yaml -r src
flake8 src
black --check src
```

---

## 2. Container Security

All Docker images must follow:
- No root user
- Minimal base image
- No hardcoded secrets
- Multi-stage builds

---

## 3. Secrets Detection

Before committing:
```
git secrets --scan
```

---

## 4. Reporting Vulnerabilities

If you discover a vulnerability:
- Do NOT open a public issue
- Include reproduction steps and severity

---

## 5. CI Integration

All scans run automatically in:
- `.github/workflows/ci.yml`

Builds failing security checks cannot be deployed.
