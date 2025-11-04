# PhishGuard Platform

PhishGuard is a modular phishing detection and response platform that combines real-time email ingestion, advanced feature engineering, machine learning, sandboxed link analysis, alerting, incident correlation, and automated response workflows.

## Repository Structure

- `services/`
  - `ingestion/`: Gmail integration, email parsing, header analysis
  - `feature_extraction/`: 50+ structural/link/content feature computation
  - `ml_engine/`: ensemble risk scoring, explainability, model lifecycle
  - `sandbox/`: isolated container orchestration, Playwright, mitmproxy
  - `alerting/`: Twilio/email notifications, WebSocket broadcaster
  - `soar/`: automated remediation playbooks (quarantine, blocklists)
  - `correlation/`: timeline reconstruction, reporting, IOC generation
- `frontend/`
  - `dashboard/`: React-based security operations console
  - `extension/`: Chrome MV3 extension for Gmail risk overlays
- `infrastructure/`
  - `docker/`: container definitions for services and sandbox workers
  - `k8s/`: Kubernetes manifests and Helm charts
  - `ci/`: CI/CD pipeline definitions and security scans
- `config/`: environment templates and shared configuration
- `docs/`: architecture diagrams, API specs, runbooks, training content
- `scripts/`: CLI helpers for development, data import/export, retraining
- `data/`: datasets, feature stores, and model artifacts (gitignored)
- `sandbox_artifacts/`: captured evidence from sandbox runs (gitignored)

## Getting Started

1. Copy `.env.example` to `.env` and adjust connection strings if needed.
2. Install Docker and start the stack: `docker compose -f infrastructure/docker/docker-compose.yml up --build`.
3. Once services are healthy, the ingestion API is available at `http://localhost:8000` and Flower at `http://localhost:5555`.
4. In a separate terminal, trigger a sample webhook: `python scripts/send_test_webhook.py`.
5. Refer to `/docs` for detailed setup guides, API documentation, and architectural references as they are completed.

## Roadmap

Development is organized into phased milestones:

1. Email ingestion & analysis
2. Feature extraction & ML detection engine
3. Sandbox automation
4. Browser extension & alerting
5. Reporting, correlation, and SOAR automations

Each milestone delivers production-ready slices that can be deployed independently and scaled via Kubernetes.
