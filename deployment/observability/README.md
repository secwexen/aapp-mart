# Deployment Observability

Use the metric names and label guidance in `observability/metrics/metrics.md`.

Operational recommendations:

- Export metrics only to an authenticated, approved monitoring system.
- Avoid including raw targets, secrets, or personal data in metric labels.
- Alert on repeated policy denials, elevated failure rates, and sustained increases in analysis duration.
- Protect audit logs with access controls and an appropriate retention policy.
- Treat hash-chain verification as tamper detection, not as a substitute for signed or immutable storage.
