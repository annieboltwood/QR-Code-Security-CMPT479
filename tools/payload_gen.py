"""
payload_gen.py — QR Code Test Suite Generator
CMPT 479 QR Code Scanner Security Study

Generates QR code PNG images from a curated set of test payloads and writes a
manifest CSV summarising every generated image.  All payloads use safe,
reserved, or clearly synthetic content — no real malicious infrastructure is
referenced.

Usage:
    pip install qrcode[pil]
    python tools/payload_gen.py

Output:
    payloads/phishing_urls/
    payloads/lookalike_domains/
    payloads/shortened_links/
    payloads/oversized_payloads/
    payloads/non_url_content/
    payloads/manifest.csv
"""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List

import qrcode

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
PAYLOADS_DIR = REPO_ROOT / "payloads"

MANIFEST_COLUMNS = [
    "id",
    "category",
    "payload_type",
    "content",
    "expected_risk",
    "filename",
    "notes",
]


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Payload:
    id: str
    category: str           # directory name under payloads/
    payload_type: str       # human-readable type label
    content: str            # exact string encoded in the QR image
    expected_risk: str      # risk label for analysis
    notes: str              # free-text annotation


# ---------------------------------------------------------------------------
# Payload definitions
# ---------------------------------------------------------------------------

def build_payloads() -> List[Payload]:
    payloads: List[Payload] = []

    # ------------------------------------------------------------------
    # 1. Phishing-style URLs
    #    Mimic patterns commonly used in credential-harvesting campaigns.
    #    All use example.com / example.org (IANA reserved, harmless).
    # ------------------------------------------------------------------
    phishing = [
        ("PHISH_001", "https://example.com/login",
         "Login page lure — canonical phishing entry point"),
        ("PHISH_002", "https://example.com/verify-account",
         "Account verification lure"),
        ("PHISH_003", "https://example.com/reset-password",
         "Password reset lure"),
        ("PHISH_004", "https://example.com/secure-login?redirect=home",
         "Login with redirect parameter — tests parameter handling"),
        ("PHISH_005", "https://example.org/update-payment-info",
         "Payment update lure — common financial phishing pattern"),
    ]
    for pid, content, notes in phishing:
        payloads.append(Payload(
            id=pid,
            category="phishing_urls",
            payload_type="phishing_url",
            content=content,
            expected_risk="phishing",
            notes=notes,
        ))

    # ------------------------------------------------------------------
    # 2. Lookalike-domain style test cases
    #    Substitute characters (1/l, 0/o) or insert hyphens to simulate
    #    typosquatting.  Domains remain within example.* / synthetic.
    # ------------------------------------------------------------------
    lookalike = [
        ("LOOK_001", "https://example.com/paypa1-login",
         "Digit '1' substituted for letter 'l' — PayPal homoglyph pattern"),
        ("LOOK_002", "https://example.org/micr0soft-verify",
         "Zero substituted for 'o' — Microsoft lookalike pattern"),
        ("LOOK_003", "https://example.net/secure-account-check",
         "Generic 'secure' prefix — common trust-signal pattern"),
        ("LOOK_004", "https://example.com/app1e-support",
         "Digit '1' for 'l' — Apple lookalike pattern"),
        ("LOOK_005", "https://example.org/arnazon-order-confirm",
         "Transposed letter — Amazon lookalike pattern"),
    ]
    for pid, content, notes in lookalike:
        payloads.append(Payload(
            id=pid,
            category="lookalike_domains",
            payload_type="lookalike_url",
            content=content,
            expected_risk="lookalike",
            notes=notes,
        ))

    # ------------------------------------------------------------------
    # 3. Short-link style URLs
    #    Opaque paths that conceal the final destination — tests whether
    #    scanners preview the resolved URL before opening.
    # ------------------------------------------------------------------
    shortened = [
        ("SHORT_001", "https://example.com/r/abc123",
         "Opaque redirect path — destination hidden from user"),
        ("SHORT_002", "https://example.com/go/reset",
         "Semantic short path — still obscures final target"),
        ("SHORT_003", "https://example.org/s/x9K2",
         "Single-letter prefix short link pattern"),
        ("SHORT_004", "https://example.com/l/Zq7mR9",
         "Mixed-case opaque token — common URL shortener format"),
        ("SHORT_005", "https://example.net/out?u=dXNlcjp0ZXN0",
         "Query-parameter redirect with base64-style token"),
    ]
    for pid, content, notes in shortened:
        payloads.append(Payload(
            id=pid,
            category="shortened_links",
            payload_type="shortened_url",
            content=content,
            expected_risk="hidden_destination",
            notes=notes,
        ))

    # ------------------------------------------------------------------
    # 4. Oversized payloads
    #    Tests scanner robustness against large inputs.  QR version 40
    #    supports up to ~4296 alphanumeric characters; payloads here
    #    exceed 1000 characters to stress input handling.
    # ------------------------------------------------------------------
    long_url_path = "a" * 980
    long_url = f"https://example.com/{'path/' * 50}{long_url_path}"

    repeated_word = "testpayload " * 90          # ~1080 chars
    long_text = repeated_word.strip()

    oversized = [
        ("OVER_001", long_url,
         "Long URL payload — path segment repeated to exceed 1000 chars"),
        ("OVER_002", long_text,
         "Plain-text payload — repeated word block exceeding 1000 chars"),
        ("OVER_003", "https://example.com/?" + "&".join(f"param{i}=value{i}" for i in range(80)),
         "URL with 80 query parameters — tests query string parsing limits"),
        ("OVER_004", "X" * 1500,
         "All-uppercase ASCII string, 1500 chars — maximum stress test"),
        ("OVER_005", ("https://example.org/deep" + "/sub" * 200),
         "Deeply nested URL path — 200 path segments"),
    ]
    for pid, content, notes in oversized:
        payloads.append(Payload(
            id=pid,
            category="oversized_payloads",
            payload_type="oversized_input",
            content=content,
            expected_risk="oversized_input",
            notes=notes,
        ))

    # ------------------------------------------------------------------
    # 5. Non-URL content
    #    Non-http(s) schemes that scanners may handle differently or
    #    execute without user confirmation.
    # ------------------------------------------------------------------
    non_url = [
        ("NONURL_001", "tel:+16045551234",
         "Telephone URI — tests whether scanner prompts before dialling"),
        ("NONURL_002", "javascript:alert('test')",
         "JavaScript URI — should never be executed; tests scheme filtering"),
        ("NONURL_003", "data:text/plain,hello-world",
         "Data URI with plain text — tests data: scheme handling"),
        ("NONURL_004", "mailto:test@example.com?subject=TestEmail",
         "Mailto URI — tests whether scanner prompts before opening mail client"),
        ("NONURL_005", "sms:+16045551234?body=TestMessage",
         "SMS URI — tests whether scanner prompts before composing SMS"),
    ]
    for pid, content, notes in non_url:
        payloads.append(Payload(
            id=pid,
            category="non_url_content",
            payload_type="non_standard_scheme",
            content=content,
            expected_risk="non_standard_scheme",
            notes=notes,
        ))

    return payloads


# ---------------------------------------------------------------------------
# QR generation helpers
# ---------------------------------------------------------------------------

def make_qr_image(content: str) -> qrcode.image.base.BaseImage:
    """Return a QR code image for *content*, using the highest error
    correction level that fits.  Falls back to lower correction levels
    for very large payloads that exceed capacity at H."""
    for error_correction in (
        qrcode.constants.ERROR_CORRECT_H,
        qrcode.constants.ERROR_CORRECT_Q,
        qrcode.constants.ERROR_CORRECT_M,
        qrcode.constants.ERROR_CORRECT_L,
    ):
        try:
            qr = qrcode.QRCode(
                error_correction=error_correction,
                box_size=10,
                border=4,
            )
            qr.add_data(content)
            qr.make(fit=True)
            return qr.make_image(fill_color="black", back_color="white")
        except qrcode.exceptions.DataOverflowError:
            continue
    raise ValueError(f"Payload too large to encode in any QR version: {content[:80]}…")


def filename_for(payload: Payload) -> str:
    """Return a safe PNG filename derived from the payload ID."""
    return f"{payload.id.lower()}.png"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    payloads = build_payloads()

    # Create output directories
    categories = {p.category for p in payloads}
    for cat in categories:
        (PAYLOADS_DIR / cat).mkdir(parents=True, exist_ok=True)

    generated = 0
    skipped = 0
    manifest_rows = []

    for payload in payloads:
        fname = filename_for(payload)
        out_path = PAYLOADS_DIR / payload.category / fname

        try:
            img = make_qr_image(payload.content)
            img.save(out_path)
            status = "OK"
            generated += 1
        except ValueError as exc:
            print(f"  [SKIP] {payload.id}: {exc}")
            status = "SKIPPED"
            skipped += 1

        manifest_rows.append({
            "id": payload.id,
            "category": payload.category,
            "payload_type": payload.payload_type,
            "content": payload.content,
            "expected_risk": payload.expected_risk,
            "filename": str(Path(payload.category) / fname),
            "notes": payload.notes,
        })

    # Write manifest CSV
    manifest_path = PAYLOADS_DIR / "manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS)
        writer.writeheader()
        writer.writerows(manifest_rows)

    # Summary
    print(f"\nPayload generation complete.")
    print(f"  Generated : {generated} QR image(s)")
    if skipped:
        print(f"  Skipped   : {skipped} (payload too large for any QR version)")
    print(f"  Manifest  : {manifest_path.relative_to(REPO_ROOT)}")
    print(f"  Output dir: {PAYLOADS_DIR.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
