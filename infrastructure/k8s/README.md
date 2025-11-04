# Kubernetes Deployment

This directory contains Helm charts and Kubernetes manifests for deploying the PhishGuard microservices.

## Components

- `base/`: Shared templates (configmaps, secrets, ingress)
- `services/`: Individual service deployments and services
- `jobs/`: CronJobs for retraining, maintenance, cleanup
- `monitoring/`: Prometheus/Grafana configuration snippets

## Deployment Workflow

1. Package secrets using `sops` or your preferred secret manager.
2. Deploy infrastructure primitives (PostgreSQL, Redis, object storage) via Helm dependencies.
3. Deploy application charts per environment (`dev`, `staging`, `prod`).
4. Configure horizontal pod autoscalers and network policies.
5. Integrate with cluster-wide observability (Prometheus, Loki, Tempo).

Sample manifests will be introduced with future iterations.

