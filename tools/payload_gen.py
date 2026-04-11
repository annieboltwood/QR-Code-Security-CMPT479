"""
Generate the final QR payload corpus for the CMPT 479 QR scanner study.

The study uses a small, deterministic set of safe payloads that probe how QR
scanner apps decode, display, validate, and hand off suspicious-looking
content. All payloads use synthetic or reserved placeholders only.

Usage:
    python3 -m venv .venv
    ./.venv/bin/pip install "qrcode[pil]"
    ./.venv/bin/python tools/payload_gen.py
"""

from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from pathlib import Path

import qrcode
from qrcode.exceptions import DataOverflowError


REPO_ROOT = Path(__file__).resolve().parent.parent
PAYLOADS_DIR = REPO_ROOT / "payloads"
MANIFEST_PATH = PAYLOADS_DIR / "manifest.csv"

MANIFEST_COLUMNS = [
    "id",
    "category",
    "payload_type",
    "content",
    "expected_behavior_or_risk",
    "filename",
    "notes",
]


@dataclass(frozen=True)
class Payload:
    id: str
    category: str
    payload_type: str
    content: str
    expected_behavior_or_risk: str
    notes: str


def build_payloads() -> list[Payload]:
    long_url = (
        "https://example.com/account-review/"
        + ("segment/" * 40)
        + ("a" * 820)
    )
    long_text = (
        "QR scanner study oversized text payload. "
        "This string is intentionally long but harmless. "
    ) * 22

    return [
        Payload(
            id="PHISH_001",
            category="phishing_style_urls",
            payload_type="url",
            content="https://example.com/login",
            expected_behavior_or_risk="Should show a clear destination preview before handoff.",
            notes="Canonical login-themed placeholder URL.",
        ),
        Payload(
            id="PHISH_002",
            category="phishing_style_urls",
            payload_type="url",
            content="https://example.org/verify-account",
            expected_behavior_or_risk="Tests whether account-themed URLs are previewed clearly and not auto-opened aggressively.",
            notes="Safe verification-themed placeholder URL.",
        ),
        Payload(
            id="PHISH_003",
            category="phishing_style_urls",
            payload_type="url",
            content="https://example.com/update-billing",
            expected_behavior_or_risk="Useful for warning and confirmation observations on finance-themed wording.",
            notes="Safe billing-themed placeholder URL.",
        ),
        Payload(
            id="DECEPT_001",
            category="deceptive_formatting",
            payload_type="url",
            content="https://example.com/paypa1-helpdesk/login",
            expected_behavior_or_risk="Tests whether lookalike-style path text is displayed in a readable way.",
            notes="Uses a harmless path with 1-for-l substitution.",
        ),
        Payload(
            id="DECEPT_002",
            category="deceptive_formatting",
            payload_type="url",
            content="https://example.org/support/microsоft-account",
            expected_behavior_or_risk="Tests handling of confusable Unicode characters in a safe placeholder URL.",
            notes="The second 'o' in 'microsоft' is Cyrillic, not Latin.",
        ),
        Payload(
            id="SHORT_001",
            category="shortened_style_links",
            payload_type="url",
            content="https://example.com/r/a8K2pQ",
            expected_behavior_or_risk="Tests whether opaque redirect-style paths are shown clearly before opening.",
            notes="Shortener-style path on a reserved placeholder domain.",
        ),
        Payload(
            id="SHORT_002",
            category="shortened_style_links",
            payload_type="url",
            content="https://example.org/out?target=acct-reset",
            expected_behavior_or_risk="Tests whether redirect-like query patterns trigger confirmation or warnings.",
            notes="Redirect-style placeholder with a readable query parameter.",
        ),
        Payload(
            id="OVER_001",
            category="oversized_payloads",
            payload_type="url",
            content=long_url,
            expected_behavior_or_risk="Exercises robustness when decoding and displaying a URL longer than 1000 characters.",
            notes="Oversized but syntactically safe URL payload.",
        ),
        Payload(
            id="OVER_002",
            category="oversized_payloads",
            payload_type="text",
            content=long_text.strip(),
            expected_behavior_or_risk="Exercises robustness when decoding and rendering plain text longer than 1000 characters.",
            notes="Oversized plain-text payload for UI and parsing stress.",
        ),
        Payload(
            id="SCHEME_001",
            category="nonstandard_schemes",
            payload_type="scheme",
            content="tel:+16045551234",
            expected_behavior_or_risk="Should not place a call without a clear prompt or controlled handoff.",
            notes="Safe telephone URI using a fictitious classroom number.",
        ),
        Payload(
            id="SCHEME_002",
            category="nonstandard_schemes",
            payload_type="scheme",
            content="data:text/plain,harmless-qr-study-payload",
            expected_behavior_or_risk="Tests whether a scanner previews or blocks a data: payload rather than handing it off blindly.",
            notes="Safe data URI containing plain text only.",
        ),
        Payload(
            id="SCHEME_003",
            category="nonstandard_schemes",
            payload_type="scheme",
            content="javascript:console.log('qr-study-harmless-string')",
            expected_behavior_or_risk="Should be rejected, treated cautiously, or at minimum not executed automatically.",
            notes="Included only as a harmless string payload for handling tests.",
        ),
    ]


def reset_output_tree(categories: set[str]) -> None:
    PAYLOADS_DIR.mkdir(parents=True, exist_ok=True)

    for child in PAYLOADS_DIR.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        elif child.name == "manifest.csv":
            child.unlink()

    for category in sorted(categories):
        (PAYLOADS_DIR / category).mkdir(parents=True, exist_ok=True)


def make_qr_image(content: str):
    for error_correction in (
        qrcode.constants.ERROR_CORRECT_Q,
        qrcode.constants.ERROR_CORRECT_M,
        qrcode.constants.ERROR_CORRECT_L,
    ):
        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=error_correction,
                box_size=10,
                border=4,
            )
            qr.add_data(content)
            qr.make(fit=True)
            return qr.make_image(fill_color="black", back_color="white")
        except (DataOverflowError, ValueError) as exc:
            if isinstance(exc, ValueError) and "Invalid version" not in str(exc):
                raise
            continue

    raise ValueError(f"Unable to encode payload {content[:80]!r} into a QR code.")


def filename_for(payload: Payload) -> str:
    return f"{payload.id.lower()}.png"


def write_manifest(payloads: list[Payload]) -> None:
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_COLUMNS)
        writer.writeheader()
        for payload in payloads:
            relative_filename = f"{payload.category}/{filename_for(payload)}"
            writer.writerow(
                {
                    "id": payload.id,
                    "category": payload.category,
                    "payload_type": payload.payload_type,
                    "content": payload.content,
                    "expected_behavior_or_risk": payload.expected_behavior_or_risk,
                    "filename": relative_filename,
                    "notes": payload.notes,
                }
            )


def main() -> None:
    payloads = build_payloads()
    categories = {payload.category for payload in payloads}
    reset_output_tree(categories)

    for payload in payloads:
        image = make_qr_image(payload.content)
        output_path = PAYLOADS_DIR / payload.category / filename_for(payload)
        image.save(output_path)

    write_manifest(payloads)
    print(f"Generated {len(payloads)} payloads in {PAYLOADS_DIR}")
    print(f"Wrote manifest to {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
