# AAPP-MART Security Scanning Guide

This document describes the security scanning standards used in the AAPP-MART project.

## 1. Static Code Analysis

The project uses automated static code analysis tools through pre-commit hooks.

Contributors are encouraged to run these checks locally before committing.

Example:
```
# Run security checks (tool names omitted for safety)
security-scan --check src
```

## 2. Container Security

All container images should follow standard security best practices:

- Avoid running as root
- Use minimal base images
- No hardcoded secrets
- Multi-stage builds

## 3. Secrets Detection

Before committing, contributors should scan for sensitive data locally.

Example:
```
# Scan for secrets
scan-secrets
```

## 4. Reporting Vulnerabilities

If you discover a vulnerability:

- Do not open a public issue
- Provide clear reproduction steps and severity internally

## 5. CI Integration

All security scans are executed automatically in the project’s CI pipeline.  
Contributors should ensure their changes pass these checks before merging.
