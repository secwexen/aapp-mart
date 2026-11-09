# Deployment

AAPP-MART should be deployed as a security analysis service with explicit authorization, restricted network access, and auditable configuration.

Before deployment:

1. Review the repository security policy and deployment settings.
2. Provide policy configuration through an approved configuration mechanism.
3. Store credentials in a secret manager; never put them in images or Git.
4. Restrict outbound network access to explicitly approved services.
5. Run the test and lint scripts in CI.
6. Confirm that audit records are retained according to your organization's policy.

The Helm chart currently contains chart metadata only. It does not create a workload or expose a service.
