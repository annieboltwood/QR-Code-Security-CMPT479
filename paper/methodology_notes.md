## Methodology

This study uses black-box evaluation to examine how QR scanner applications decode, display, validate, and hand off suspicious-looking but safe payloads in practice. Black-box testing is appropriate given the project's goal: to characterize user-visible and network-visible behavior of deployed scanners rather than audit source code or verify internal implementation correctness.

**Payload corpus.** The test corpus spans five categories — phishing-style URLs, deceptive or lookalike formatting, shortened-style links, oversized payloads, and nonstandard URI schemes — using only synthetic content on placeholder domains. No live phishing infrastructure or active exploit payloads were used at any stage.

**Evaluation criteria.** Each payload–app combination is assessed across four dimensions: destination preview clarity, confirmation versus auto-open behavior, parsing robustness, and third-party network leakage.

**Target applications.** Three Android apps were selected: QR & Barcode Scanner (Gamma Play), Binary Eye, and QR Code & Barcode Scanner Plus. This set was chosen to fit the project timeline while offering a meaningful contrast between a mainstream scanner, an open-source privacy-oriented alternative, and a consumer-facing standalone product.

**Testing environment.** All scans were conducted in an Android emulator for repeatability. Network traffic was observed with mitmproxy; Wireshark was used for packet-level capture where needed. Observations were recorded manually in `data/results.csv`, notable screenshots were saved alongside each session, and running notes were maintained in `docs/test_log.md`.

**Limitations.** The study has several important constraints: a small payload sample, Android-only scope, emulator-based testing (rather than physical devices), no systematic claims about true malicious-URL classification quality, and limited time for repeated trials across app versions or hardware configurations.