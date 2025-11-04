"""Gmail client helpers (stubbed for local development)."""

from __future__ import annotations

from textwrap import dedent


def get_gmail_message(message_id: str) -> bytes:
    """Return a raw RFC822 message for the provided Gmail message ID."""

    # TODO: replace stub with googleapiclient discovery calls using OAuth credentials.
    sample_email = dedent(
        f"""
        From: Example Sender <sender@example.com>
        To: Recipient <recipient@example.com>
        Subject: Test message for {message_id}
        Message-Id: <{message_id}@example.com>
        Date: Tue, 04 Nov 2025 10:00:00 +0000
        MIME-Version: 1.0
        Content-Type: multipart/alternative; boundary="000000"

        --000000
        Content-Type: text/plain; charset="utf-8"

        This is a plain text version of the email.
        Visit https://secure.example.com for more details.

        --000000
        Content-Type: text/html; charset="utf-8"

        <html>
          <body>
            <p>This is a <strong>sample email</strong>.</p>
            <p>Click <a href="https://secure.example.com/reset">here</a> to reset your account.</p>
          </body>
        </html>

        --000000--
        """
    ).strip()

    return sample_email.encode("utf-8")

