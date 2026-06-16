#!/usr/bin/env python3
"""
Fetch Productboard notes in batches and write link, optional Freshdesk URL, and body to CSV.
Uses GET /notes with pagination; respects 429 and Retry-After.
Body is stripped of HTML tags (plain text).
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load .env from script directory so PRODUCTBOARD_API_TOKEN can be set there
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# Set FRESHDESK_URL_PREFIX to your company's Freshdesk domain (or override via env)
FRESHDESK_URL_PREFIX = os.environ.get("FRESHDESK_URL_PREFIX", "https://your-company.freshdesk.com")


def strip_html(html: str) -> str:
    """Return plain text with HTML tags removed."""
    if not html:
        return ""
    return BeautifulSoup(html, "html.parser").get_text(separator=" ", strip=True)


def get_freshdesk_url(html: str) -> str:
    """Return the first <a href="...freshdesk.com..."> URL, or empty string."""
    if not html or FRESHDESK_URL_PREFIX not in html:
        return ""
    # Allow href="url", href='url', or href=""url"" (double-quoted value)
    escaped = re.escape(FRESHDESK_URL_PREFIX)
    m = re.search(
        r'href\s*=\s*["\']*"?\s*(' + escaped + r'[^"\'>\s]*)',
        html,
        re.IGNORECASE,
    )
    return m.group(1) if m else ""


def strip_leading_freshdesk_url(body_text: str, freshdesk_url: str) -> str:
    """Remove freshdesk_url and following whitespace from the start of body_text, only if it appears at the beginning."""
    if not freshdesk_url or not body_text:
        return body_text
    trimmed = body_text.lstrip()
    if trimmed.startswith(freshdesk_url):
        rest = trimmed[len(freshdesk_url) :].lstrip()
        return rest
    return body_text


def extract_ticket_title(body_text: str) -> tuple[str, str]:
    """If body ends with 'Ticket NNNNN: <title>', return (body_without_that_suffix, title). Else return (body_text, '')."""
    if not body_text:
        return body_text, ""
    m = re.search(r"Ticket\s+\d+:\s*(.+)\s*$", body_text, re.DOTALL)
    if not m:
        return body_text, ""
    ticket_title = m.group(1).strip()
    body_without = body_text[: m.start()].rstrip()
    return body_without, ticket_title


BASE_URL = "https://api.productboard.com"
NOTES_PATH = "/notes"


def make_request(url: str, token: str) -> tuple[dict, int]:
    """GET url with Bearer token. Returns (response_body, status_code)."""
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read().decode())
        return body, resp.status


def fetch_notes_page(token: str, page_limit: int, page_cursor: str | None) -> tuple[list, str | None]:
    """
    Fetch one page of notes. Returns (list of note dicts, next_page_cursor or None).
    On 429, waits Retry-After then retries once.
    """
    params = [("pageLimit", page_limit)]
    if page_cursor:
        params.append(("pageCursor", page_cursor))
    qs = "&".join(f"{k}={v}" for k, v in params)
    url = f"{BASE_URL}{NOTES_PATH}?{qs}"

    for attempt in range(2):
        try:
            body, status = make_request(url, token)
        except urllib.error.HTTPError as e:
            body = None
            status = e.code
            if status == 429:
                retry_after = e.headers.get("Retry-After", "60")
                try:
                    wait = int(retry_after)
                except ValueError:
                    wait = 60
                if attempt == 0:
                    time.sleep(wait)
                    continue
            raise
        except urllib.error.URLError as e:
            print(f"Request failed: {e}", file=sys.stderr)
            raise

        if status != 200:
            raise RuntimeError(f"API returned {status}: {body}")

        data = body.get("data", [])
        next_cursor = body.get("pageCursor")
        return data, next_cursor


def run(token: str, output_path: str, max_notes: int | None, page_limit: int) -> None:
    """Fetch notes and stream rows to CSV."""
    cursor = None
    total_written = 0

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["link", "createdAt", "Freshdesk URL", "body", "Ticket Title"])

        while True:
            notes, cursor = fetch_notes_page(token, page_limit, cursor)
            if not notes:
                break

            for note in notes:
                if max_notes is not None and total_written >= max_notes:
                    return
                link = note.get("displayUrl") or ""
                created_at = note.get("createdAt") or ""
                body = note.get("content") or ""
                freshdesk_url = get_freshdesk_url(body)
                stripped = strip_html(body)
                body_no_fd = strip_leading_freshdesk_url(stripped, freshdesk_url)
                body_cleaned, ticket_title = extract_ticket_title(body_no_fd)
                writer.writerow([link, created_at, freshdesk_url, body_cleaned, ticket_title])
                total_written += 1

            if not cursor or (max_notes is not None and total_written >= max_notes):
                break


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Productboard notes to CSV (link, createdAt, Freshdesk URL, body, Ticket Title).")
    parser.add_argument(
        "--token",
        default=os.environ.get("PRODUCTBOARD_API_TOKEN"),
        help="API token (default: PRODUCTBOARD_API_TOKEN)",
    )
    parser.add_argument(
        "--output", "-o",
        default="notes.csv",
        help="Output CSV path (default: notes.csv)",
    )
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=None,
        help="Max number of notes to fetch (default: all)",
    )
    parser.add_argument(
        "--page-limit",
        type=int,
        default=100,
        help="Notes per API request (default: 100)",
    )
    args = parser.parse_args()

    if not args.token:
        print("Set PRODUCTBOARD_API_TOKEN or pass --token", file=sys.stderr)
        return 1

    run(args.token, args.output, args.limit, args.page_limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
