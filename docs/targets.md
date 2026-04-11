# Testing Targets

The final study uses exactly three Android QR scanner applications. This keeps
the project practical for a short deadline while still providing meaningful
contrast between mainstream, open-source/privacy-oriented, and
security-positioned scanner behavior.

## Target Set

### QR & Barcode Scanner (Gamma Play)

- Type: mainstream standalone Android scanner
- Justification: serves as the baseline for how a popular dedicated scanner
  presents destinations, asks for confirmation, and hands off decoded payloads
  in a typical consumer app workflow

### Binary Eye

- Type: open-source and privacy-oriented Android scanner
- Justification: provides a useful comparison point for whether a scanner with a
  more privacy-conscious and transparent design philosophy behaves differently
  from a mainstream Play Store scanner

### Trend Micro QR Scanner

- Type: security-oriented Android scanner
- Justification: provides an explicit security-focused comparison target because
  it markets dangerous-link and safe-browsing style protection, making it
  relevant to warning, preview, and handoff behavior

## Why These Three

This target set is intentionally small because the team has roughly one day of
effort remaining. The three selected apps are easy to install and test in an
Android emulator, and together they offer enough contrast to support a credible
black-box comparison without expanding the study beyond what can be defended in
the final paper.
