"""Send a sample Gmail webhook payload to the local ingestion service."""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import logging
from typing import Any

import httpx


logger = logging.getLogger(__name__)


def build_sample_payload(message_id: str) -> dict[str, Any]:
    envelope = {"messageId": message_id}
    encoded = base64.urlsafe_b64encode(json.dumps(envelope).encode("utf-8")).decode("utf-8")
    return {
        "message": {
            "data": encoded,
            "messageId": message_id,
        },
        "subscription": "projects/dev/subscriptions/gmail-ingestion",
    }


async def send_webhook(url: str, message_id: str) -> None:
    payload = build_sample_payload(message_id)
    headers = {"X-Google-Signature": "dev-signature"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logger.info("Webhook accepted: %s", response.json())
        print(json.dumps(response.json(), indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--url",
        default="http://localhost:8000/webhook/gmail",
        help="Target webhook URL.",
    )
    parser.add_argument(
        "--message-id",
        default="local-test-message",
        help="Gmail message id to include in the sample payload.",
    )
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    asyncio.run(send_webhook(args.url, args.message_id))


if __name__ == "__main__":
    main()

