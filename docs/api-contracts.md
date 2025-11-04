# API Contracts

This document captures the high-level API contracts exposed by the PhishGuard microservices. Detailed OpenAPI schemas will be generated programmatically from each FastAPI service.

## Ingestion Service

- `POST /gmail/push/webhook`
  - **Description**: Receives Gmail push notifications, validates JWT, and enqueues message retrieval tasks.
  - **Auth**: Google-signed JWT validation.
  - **Response**: `204 No Content`.
- `POST /emails/{message_id}/ingest`
  - **Description**: Fetches the email via Gmail API, parses metadata, and stores normalized entities.
  - **Auth**: Internal JWT.
  - **Response**: `{ "message_id": string, "status": "queued" }`.

## Feature Extraction Service

- `POST /features/extract`
  - **Body**: `{ "message_id": string, "payload": { ... } }`
  - **Response**: Extracted feature vector metadata and persistence confirmation.
- `GET /features/{message_id}`
  - **Response**: Feature vector and derivation metadata.

## ML Engine Service

- `POST /ml/score`
  - **Body**: `{ "message_id": string, "features": { ... } }`
  - **Response**: `{ "score": float, "confidence": float, "explanations": [ ... ] }`.
- `GET /ml/models`
  - **Response**: List of deployed models and metadata.

## Sandbox Service

- `POST /sandbox/run`
  - **Body**: `{ "url": string, "message_id": string }`
  - **Response**: `{ "sandbox_id": string, "status": "scheduled" }`.
- `GET /sandbox/{sandbox_id}`
  - **Response**: Status, artifacts, risk signals.

## Alerting Service

- `POST /alerts/notify`
  - **Body**: `{ "channel": "sms"|"email"|"websocket", "payload": { ... } }`
  - **Response**: `{ "status": "queued" }`.
- WebSocket `/ws/alerts`
  - **Payload**: Risk updates, sandbox statuses, analyst notifications.

## SOAR Service

- `POST /soar/playbooks/{playbook_id}/trigger`
  - **Body**: Playbook parameters.
  - **Response**: Execution identifier and status.

## Correlation Service

- `GET /incidents/{incident_id}`
  - **Response**: Full incident timeline, related emails, sandbox sessions, IOCs.
- `POST /incidents/report`
  - **Body**: Reporting parameters.
  - **Response**: Link to generated PDF and IOC bundle.

