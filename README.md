# QR Code Scanner Security Study

Black-box security evaluation for a CMPT 479 project at Simon Fraser University.
The study asks: **How safely do QR scanner implementations decode, display,
validate, and hand off suspicious QR payloads in practice?**

This repository is intentionally narrow. It is **not** a project about breaking
TLS, defeating browser safe browsing, or deciding whether a URL is truly
malicious. The focus is the scanner's behavior before and during handoff after a
QR payload is decoded.

## Team

- Jedidiah Akinola
- Annie Boltwood
- Mahim Chaudhary

## Study Scope

We evaluate scanner behavior along four dimensions:

- destination preview clarity
- confirmation versus aggressive auto-open behavior
- parsing robustness for unusual but safe payloads
- third-party leakage during scanning or handoff

The fixed Android targets for the final project scope are:

- **QR & Barcode Scanner (Gamma Play)** — mainstream standalone scanner baseline
- **Binary Eye** — open-source and privacy-oriented comparison target
- **QR Code & Barcode Scanner Plus** — practical third-party comparison target
  that adds another easy-to-test standalone scanner for comparison of preview,
  confirmation, and handoff behavior

This target set was chosen because it is easy to test under a short deadline
while still giving useful behavioral contrast.

## Repository Structure

This repo is organized around a small, reproducible manual testing workflow:

- `tools/payload_gen.py`: generates the final study payload set as QR images.
- `payloads/`: generated QR PNGs grouped by category, plus
  `payloads/manifest.csv` describing every payload.
- `data/results.csv`: blank results sheet for manual observations across all
  target apps and payloads.
- `data/screenshots/`: notable screenshots captured during testing.
- `data/captures/`: network captures or proxy exports used for leakage checks.
- `docs/targets.md`: the fixed set of three Android scanner targets and why
  they were chosen.
- `docs/testing_plan.md`: high-level test matrix and expected scan volume.
- `docs/test_log.md`: reusable session log template for each testing run.
- `docs/setup.md`: Android emulator, mitmproxy, and Wireshark setup notes.
- `paper/methodology_notes.md`: methodology skeleton for the paper.
- `paper/findings_notes.md`: findings template for writing up observations.

## Generating Payloads

The payloads are already generated in this repository. You only need to run the
generator if you want to rebuild them.

To regenerate the QR corpus:

```bash
python3 -m venv .venv
./.venv/bin/pip install "qrcode[pil]"
./.venv/bin/python tools/payload_gen.py
```

The script produces a small, deterministic corpus of about 12 safe,
classroom-appropriate payloads across phishing-style URLs, deceptive
formatting, shortened-style links, oversized payloads, and nonstandard schemes.
All content uses reserved or synthetic placeholders only.

## How To Use The Repo

For the final project workflow:

1. Use the existing QR images in `payloads/` or regenerate them with
   `tools/payload_gen.py`.
2. Install and test the three target Android apps listed in `docs/targets.md`.
3. Scan each payload in each target app.
4. Record observations in `data/results.csv`.
5. Save notable screenshots in `data/screenshots/` and relevant traffic
   captures in `data/captures/`.
6. Use the notes in `paper/` and `docs/` when drafting the final report.

## Recording Results

- Log per-scan observations in `data/results.csv`.
- Use `docs/test_log.md` for session-level notes and anomalies.
- Save screenshots that capture notable behavior in `data/screenshots/`.
- Save packet captures or proxy exports in `data/captures/`.

## Reproducibility Artifacts

This repository includes the payload generator, generated QR codes, the payload
manifest, target documentation, manual testing templates, setup notes, and
paper-note skeletons needed to reproduce the final scoped study.
