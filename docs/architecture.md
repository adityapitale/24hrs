# Architecture Overview

PhishGuard is composed of modular microservices that communicate over asynchronous queues (Celery/Redis) and REST APIs (FastAPI). The platform is designed for horizontal scalability, high observability, and strong security controls.

## High-Level Components

- **Email Ingestion Service**: Handles Gmail OAuth, push notifications, MIME parsing, and normalization of headers, body, links, and attachments.
- **Feature Extraction Service**: Derives 50+ structural, link-based, and content-based features including DNS/WHOIS lookups, SSL inspections, NLP signals, image/attachment metadata.
- **ML Engine Service**: Provides risk scoring via ensemble classifiers (Random Forest, Gradient Boosting, heuristic voting) with explainability payloads (SHAP/LIME).
- **Sandbox Orchestrator**: Spins isolated Docker containers with Playwright-driven browsers, mitmproxy interception, and evidence capture (screenshots, HAR, PCAP, DOM diffs).
- **Alerting Service**: Publishes WebSocket updates to the dashboard and triggers Twilio/SMS/email alerts based on configurable thresholds.
- **SOAR Service**: Automates remediation playbooks (quarantine email, revoke tokens, block domains) and integrates with SIEM/TI platforms.
- **Correlation & Reporting Service**: Links sandbox sessions to originating emails, maintains incident timelines, and generates PDF reports with IOC exports.
- **Frontend Dashboard**: React application for security analysts with live metrics, incident triage, feedback loops, and performance dashboards.
- **Browser Extension**: Chrome Manifest V3 extension injecting risk badges and sandbox triggers into the Gmail UI.

## Data Flow

1. Gmail push notification hits the ingestion webhook.
2. Email metadata is parsed, stored, and dispatched via Celery to the feature extraction pipeline.
3. Aggregated features are persisted to PostgreSQL and evaluated by the ML engine.
4. Risk scores are cached in Redis and surfaced to frontend clients via WebSockets.
5. Links exceeding 30% risk spawn sandbox jobs. Artifacts are stored in object storage and correlated back to the incident.
6. Alerts and SOAR actions are triggered based on configurable thresholds and analyst feedback.
7. Continuous feedback feeds retraining and rule A/B testing.

## Deployment

- Docker images for each microservice supporting dev, staging, prod environments.
- Kubernetes (K8s) deployment via Helm charts with HPA, PodSecurityPolicies, and service meshes (optional).
- Centralized logging (ELK/EFK), metrics (Prometheus/Grafana), and tracing (OpenTelemetry).

## Security Safeguards

- JWT-based service-to-service auth with role-based access in the dashboard.
- TLS termination at ingress, mutual TLS between services (optional), and secrets management via Vault or K8s secrets.
- Sandbox isolation with network egress controls, resource quotas, and automated teardown.
- Periodic security scans integrated into CI/CD.

