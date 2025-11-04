"""FastAPI entrypoint for the email ingestion service."""

from __future__ import annotations

import base64
import json
import logging
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import get_db
from .gmail.client import get_gmail_message
from .models.db import Email
from .parsing.mime_parser import parse_raw_email
from .schemas.email import GmailPush
from .tasks.publish_features import extract_features


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify_google_signature(signature: str | None, body: bytes) -> bool:
    """Stub verification for Gmail webhook signatures."""

    _ = body  # placeholder to silence unused parameter while signature checks are stubbed.
    if not signature:
        logger.warning("Missing X-Google-Signature header; accepting in development mode")
    # TODO: replace with HMAC verification using shared secret or Google certificates.
    return True


def _extract_message_id(payload: GmailPush) -> tuple[str | None, dict[str, Any] | None]:
    """Derive the Gmail message ID from the push notification payload."""

    message_id = payload.message_id
    decoded_data: dict[str, Any] | None = None

    if payload.message:
        message_id = message_id or payload.message.message_id
        if payload.message.data:
            try:
                decoded_bytes = base64.urlsafe_b64decode(payload.message.data + "==")
                decoded_str = decoded_bytes.decode("utf-8")
                decoded_data = json.loads(decoded_str)
                message_id = decoded_data.get("messageId") or message_id
            except (ValueError, json.JSONDecodeError):
                logger.exception("Failed to decode Gmail push payload data")

    return message_id, decoded_data


def create_app() -> FastAPI:
    """Create the FastAPI application instance."""

    app = FastAPI(title="PhishGuard Ingestion Service", version="0.1.0")

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/webhook/gmail", status_code=status.HTTP_202_ACCEPTED, tags=["webhooks"])
    async def gmail_webhook(
        payload: GmailPush,
        x_google_signature: str | None = Header(default=None, alias="X-Google-Signature"),
        db: AsyncSession = Depends(get_db),
    ) -> dict[str, Any]:
        raw_body = payload.model_dump_json(by_alias=True).encode("utf-8")
        if not verify_google_signature(x_google_signature, raw_body):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

        message_id, decoded_data = _extract_message_id(payload)
        if not message_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing message ID")

        logger.info("Received Gmail push notification for message_id=%s", message_id)

        raw_message_bytes = get_gmail_message(message_id)
        normalized = parse_raw_email(raw_message_bytes)
        if normalized.message_id != message_id:
            normalized = normalized.copy(update={"message_id": message_id})

        email_record = Email(
            message_id=normalized.message_id,
            sender=normalized.sender,
            subject=normalized.subject,
            headers=normalized.headers,
            text_body=normalized.text_body,
            html_body=normalized.html_body,
            links=normalized.links,
            attachments=normalized.attachments,
            received_at=normalized.received_at,
            raw_payload=payload.model_dump(by_alias=True),
        )

        db.add(email_record)
        await db.flush()
        await db.commit()
        await db.refresh(email_record)

        extract_features.delay(email_record.id)
        logger.info("Persisted email_id=%s and enqueued feature extraction", email_record.id)

        response_payload: dict[str, Any] = {
            "email_id": email_record.id,
            "message_id": email_record.message_id,
        }
        if decoded_data:
            response_payload["pubsub_message"] = decoded_data

        return response_payload

    return app


app = create_app()


