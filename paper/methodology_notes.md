# Methodology Notes

- Final framing: this is a black-box security evaluation of how QR scanner apps
  decode, display, validate, and hand off suspicious-looking but safe payloads
  in practice.
- Black-box testing is appropriate because the project goal is to study
  user-visible and network-visible behavior of deployed scanners, not to audit
  source code or prove internal implementation correctness.
- Payload categories in the final corpus are phishing-style URLs, deceptive or
  lookalike formatting, shortened-style links, oversized payloads, and
  nonstandard schemes.
- Evaluation criteria are destination preview clarity, confirmation versus
  auto-open behavior, parsing robustness, and third-party leakage.
- Testing setup: Android emulator for repeatable scanner testing, mitmproxy for
  observing app and handoff traffic, and Wireshark for packet-level capture when
  needed.
- Fixed target apps: QR & Barcode Scanner (Gamma Play), Binary Eye, and Trend
  Micro QR Scanner.
- Practical workflow: scan each payload in each target, record manual
  observations in `data/results.csv`, save notable screenshots, and keep
  session-level notes in `docs/test_log.md`.
- Scope control: the corpus uses only safe synthetic content on placeholder
  domains and harmless URI strings; it does not rely on live phishing
  infrastructure or active exploit payloads.
- Limitations: small sample size, Android-only scope, emulator-based testing,
  no claims about true malicious-URL classification quality, and limited time
  for repeated trials across versions or devices.
