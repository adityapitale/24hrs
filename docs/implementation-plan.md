# Implementation Plan

This roadmap breaks the delivery into fortnightly milestones aligned with the requested priorities.

## Weeks 1-2: Email Ingestion & Analysis

- Establish Gmail OAuth 2.0 integration, token storage, and refresh handling.
- Configure Gmail watch API and push notification webhook with signature validation.
- Implement MIME parsing pipeline extracting sender, headers (SPF/DKIM/DMARC), subject, body, links, attachments.
- Normalize HTML/Plaintext bodies, sanitize inputs, and compute preliminary structural features.
- Persist emails and metadata in PostgreSQL; enqueue Celery tasks for downstream processing.

## Weeks 3-4: Feature Extraction & ML Engine

- Build modular feature computation engine covering structural, link, and content feature classes (50+ total).
- Integrate DNS, WHOIS, SSL analysis, and domain reputation lookups with caching.
- Implement NLP and attachment analysis (hashing, file type detection, optional VirusTotal lookup stubs).
- Construct training dataset pipelines, baseline Random Forest, and ensemble strategy.
- Expose scoring API with real-time risk/confidence outputs and SHAP/LIME explanations.

## Weeks 5-6: Sandboxed Link Analysis

- Design Docker-based sandbox templates with resource limits and disposal policies.
- Integrate Playwright headless browser automation, mitmproxy network capture, and artifact storage.
- Implement behavioral heuristics (form submission, JS execution, file download detection).
- Provide APIs for sandbox scheduling, status polling, and artifact retrieval.

## Weeks 7-8: Browser Extension & Alerting

- Develop Chrome MV3 extension with Gmail DOM augmentation and risk badges.
- Implement WebSocket client for live risk updates and sandbox triggers.
- Build alerting service for Twilio SMS, email notifications, and analyst escalation flows.
- Integrate React dashboard with incidents list, detail view, sandbox evidence, and feedback submission.

## Weeks 9-10: Reporting, Correlation, SOAR, Continuous Learning

- Build correlation engine to link emails, sandbox sessions, and user actions into timelines.
- Generate automated PDF reports with executive summary, technical insights, IOCs, and mitigation steps.
- Implement SOAR playbooks: Gmail quarantine, domain blocking, OAuth token revocation, SIEM/TI sync.
- Develop analyst feedback interface, automate weekly model retraining jobs, and track metrics (detection rate, false positive rate, MTTR).
- Publish dashboards for trends, behavior analytics, and A/B testing of detection rules.

## Cross-Cutting Concerns

- Infrastructure-as-code for Docker/K8s, CI/CD pipelines, monitoring, and logging.
- Security hardening guides, API authentication (JWT), data encryption, rate limiting, and audit logging.
- Documentation and training materials for analysts and administrators.

