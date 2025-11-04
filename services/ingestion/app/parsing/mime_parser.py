"""Utilities for parsing raw RFC822 emails into normalized structures."""

from __future__ import annotations

from email import message_from_bytes
from email.header import decode_header
from email.message import Message
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import tldextract

from ..schemas.email import NormalizedEmailCreate


def _decode_header(value: str | None) -> str | None:
    if not value:
        return None
    decoded_parts = []
    for fragment, encoding in decode_header(value):
        if isinstance(fragment, bytes):
            encoding = encoding or "utf-8"
            try:
                decoded_parts.append(fragment.decode(encoding, errors="replace"))
            except LookupError:  # pragma: no cover - unexpected encodings
                decoded_parts.append(fragment.decode("utf-8", errors="replace"))
        else:
            decoded_parts.append(fragment)
    return "".join(decoded_parts)


def _extract_bodies(message: Message) -> tuple[str | None, str | None]:
    text_body: str | None = None
    html_body: str | None = None

    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            disposition = part.get_content_disposition()
            if disposition == "attachment":
                continue
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            decoded = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
            if content_type == "text/plain" and text_body is None:
                text_body = decoded
            elif content_type == "text/html" and html_body is None:
                html_body = decoded
    else:
        payload = message.get_payload(decode=True)
        if payload is not None:
            decoded = payload.decode(message.get_content_charset() or "utf-8", errors="replace")
            if message.get_content_type() == "text/html":
                html_body = decoded
            else:
                text_body = decoded

    if html_body and not text_body:
        soup = BeautifulSoup(html_body, "html.parser")
        text_body = soup.get_text(separator="\n")

    return text_body, html_body


def _extract_links(html_body: str | None) -> list[str]:
    if not html_body:
        return []

    soup = BeautifulSoup(html_body, "html.parser")
    links: list[str] = []
    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href")
        if not href:
            continue
        parsed = urlparse(href)
        if not parsed.scheme:
            continue
        _domain = tldextract.extract(parsed.netloc).registered_domain
        # TODO: persist domain-level insights alongside full URLs for link analysis.
        links.append(href)
    return links


def _extract_attachments(message: Message) -> list[dict[str, Any]]:
    attachments: list[dict[str, Any]] = []
    for part in message.walk():
        disposition = part.get_content_disposition()
        if disposition != "attachment":
            continue
        payload = part.get_payload(decode=True) or b""
        attachments.append(
            {
                "filename": part.get_filename(),
                "content_type": part.get_content_type(),
                "size": len(payload),
            }
        )
    return attachments


def parse_raw_email(raw_message_bytes: bytes) -> NormalizedEmailCreate:
    """Parse a raw RFC822 message into a normalized structure."""

    message = message_from_bytes(raw_message_bytes)

    message_id = _decode_header(message.get("Message-Id")) or "unknown-message-id"
    sender = _decode_header(message.get("From"))
    subject = _decode_header(message.get("Subject"))
    received_at = None
    if message.get("Date"):
        try:
            received_at = parsedate_to_datetime(message.get("Date"))
        except (TypeError, ValueError):  # pragma: no cover - guard against malformed dates
            received_at = None

    text_body, html_body = _extract_bodies(message)
    links = _extract_links(html_body)
    attachments = _extract_attachments(message)

    headers = {key: value for key, value in message.items()}

    # TODO: integrate SPF/DKIM/DMARC validation using dedicated libraries.

    return NormalizedEmailCreate(
        message_id=message_id,
        sender=sender,
        subject=subject,
        headers=headers,
        text_body=text_body,
        html_body=html_body,
        links=links,
        attachments=attachments,
        received_at=received_at,
    )

