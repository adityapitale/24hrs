"""Pydantic schemas for Gmail webhook payloads and normalized emails."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class GmailPushMessage(BaseModel):
    """Subset of Gmail Pub/Sub push message payload."""

    data: str | None = None
    message_id: str | None = Field(default=None, alias="messageId")
    publish_time: datetime | None = Field(default=None, alias="publishTime")
    attributes: dict[str, Any] | None = None


class GmailPush(BaseModel):
    """Top-level Gmail webhook body."""

    message: GmailPushMessage | None = None
    subscription: str | None = None
    message_id: str | None = Field(default=None, alias="messageId")

    class Config:
        allow_population_by_field_name = True


class NormalizedEmailCreate(BaseModel):
    """Normalized email payload ready for persistence."""

    message_id: str
    sender: str | None = None
    subject: str | None = None
    headers: dict[str, Any]
    text_body: str | None = None
    html_body: str | None = None
    links: list[str]
    attachments: list[dict[str, Any]]
    received_at: datetime | None = None

