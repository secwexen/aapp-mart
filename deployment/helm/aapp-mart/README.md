# AAPP-MART Helm Chart

This chart currently contains metadata only. It intentionally defines no Kubernetes workloads, services, ingress rules, or permissions.

Validate the chart metadata with Helm:

```bash
helm lint deployment/helm/aapp-mart
```

Do not treat this chart as a deployable service until workload templates, security context, resource limits, authentication, and network restrictions have been reviewed and tested.
