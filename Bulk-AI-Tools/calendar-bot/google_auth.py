"""This file signs in to Google for the Calendar, Docs, and Drive writers.

It keeps sign-in in one place, so each writer can focus on saving its output.
The small command-line option is useful when this computer has
no browser: it prints a sign-in link while the local callback server waits.
An existing token keeps the scopes it was originally granted, while a fresh
sign-in asks for the three destinations this bot writes. Saved details are written
only after the token file is made private.
"""

import argparse
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]
PROJECT = Path(__file__).resolve().parent


def get_google_service(api: str, version: str, credentials_path: Path, token_path: Path,
                       *, authorize: bool = False, open_browser: bool = True):
    """Load the saved grant and connect one writer to its Google API."""
    credentials_path = Path(credentials_path)
    token_path = Path(token_path)
    credentials = None

    if token_path.exists():
        # Let Google's saved token keep its original grant. Passing SCOPES here
        # would narrow older tokens and can make their refresh request invalid.
        credentials = Credentials.from_authorized_user_file(str(token_path))

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    elif not credentials or not credentials.valid:
        if not authorize:
            raise RuntimeError(f"Google sign-in is required. Run `python {Path(__file__).resolve()}` first.")
        flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
        credentials = flow.run_local_server(
            host="127.0.0.1",
            port=0,
            open_browser=open_browser,
            authorization_prompt_message="Open this link to sign in: {url}",
            success_message="Google sign-in is complete. You can close this tab.",
        )

    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_fd = os.open(token_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.fchmod(token_fd, 0o600)
    with os.fdopen(token_fd, "w", encoding="utf-8") as token_file:
        token_file.write(credentials.to_json())
    return build(api, version, credentials=credentials)


def get_calendar_service(credentials_path: Path, token_path: Path, **options):
    """Keep the Calendar writer's small sign-in call in one place."""
    return get_google_service("calendar", "v3", credentials_path, token_path, **options)


def main():
    """Offer a standalone sign-in step that can run before processing jobs."""
    parser = argparse.ArgumentParser(description="Sign in to Google Calendar, Docs, and Drive.")
    parser.add_argument("--credentials", type=Path, default=PROJECT / "credentials.json")
    parser.add_argument("--token", type=Path, default=PROJECT / "token.json")
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Print the sign-in link instead of trying to open a browser.",
    )
    args = parser.parse_args()
    get_calendar_service(args.credentials, args.token, authorize=True, open_browser=not args.no_browser)
    print(f"Google token saved to {args.token}")


if __name__ == "__main__":
    main()
