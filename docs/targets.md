# Testing Targets — QR Code Scanner Security Study

This document defines the five targets selected for our black-box security evaluation of Android QR code scanners. Each target was chosen deliberately to give the study broad coverage across scanner types, implementation approaches, and real-world usage patterns.

---

## Selection Criteria

We selected targets based on the following principles:

- **Mix of popular and open-source**: We include scanners with large real-world user bases alongside widely used open-source libraries, so findings are relevant to both end users and developers.
- **Android-emulator compatibility**: All targets can be tested within our Mac + Android Studio (Pixel 6) workflow without requiring physical hardware or additional platform setup.
- **Variety in implementation style**: Targets differ in how they are built and how they handle QR content, allowing us to compare behavior across first-party, third-party, and library-based systems.
- **Diversity in trust model**: By including a Google-integrated scanner, independent third-party apps, and bare libraries, we can assess how the scanner's origin and integration level affects its security posture.

---

## Targets

### 1. Google Lens / Google App (Android)

| Field    | Detail                      |
|----------|-----------------------------|
| Type     | Mainstream / first-party app |
| Platform | Android                     |

**Justification:** Google Lens is deeply integrated into Android and represents how a large segment of users encounter QR scanning in practice. As a first-party Google product, it is worth evaluating whether it applies stricter URL validation or user warnings compared to independent apps. Its behavior sets a useful baseline for the study.

---

### 2. QR & Barcode Scanner by TeaCapps

| Field    | Detail                        |
|----------|-------------------------------|
| Type     | Standalone third-party app    |
| Platform | Android (Google Play)         |

**Justification:** TeaCapps' scanner is one of the most widely installed dedicated QR scanner apps on the Play Store, with tens of millions of installs. Its large install base makes it a high-priority target — any security gaps affect a significant real-world population. It also provides a comparison point against Google's integrated scanner.

---

### 3. QR & Barcode Scanner by Gamma Play

| Field    | Detail                        |
|----------|-------------------------------|
| Type     | Standalone third-party app    |
| Platform | Android (Google Play)         |

**Justification:** Gamma Play's scanner is another high-popularity standalone app. Including two independent third-party scanners allows us to compare behavior between apps of the same category, identifying whether differences in URL handling, auto-open behavior, or data transmission are app-specific choices or patterns shared across this class of scanner.

---

### 4. ZXing ("Zebra Crossing")

| Field    | Detail                        |
|----------|-------------------------------|
| Type     | Open-source library / app     |
| Platform | Android                       |

**Justification:** ZXing is the most widely used open-source barcode and QR decoding library in the Android ecosystem. Many third-party apps are built on top of it. Evaluating ZXing directly — via its reference Android app — lets us assess baseline library behavior before higher-level application logic is applied. It is also a relevant target because vulnerabilities in ZXing can have downstream effects on any app that depends on it.

---

### 5. ZBar

| Field    | Detail                        |
|----------|-------------------------------|
| Type     | Open-source library           |
| Platform | Cross-platform (Android-accessible via wrapper) |

**Justification:** ZBar is an alternative open-source barcode reading library with its own parsing implementation. Including it alongside ZXing allows us to compare how two different decoding engines handle malformed, oversized, or adversarially crafted QR payloads. Differences in how each library processes encoded content may reveal implementation-specific weaknesses.

---

## Note on iOS Camera

The native iOS Camera app is not included as a primary target in this study. Our testing environment is built around the Mac + Android Studio emulator workflow, and adding iOS would require a physical iPhone (the iOS Simulator does not support camera-based QR scanning), which introduces significant additional setup overhead for a black-box testing methodology. If a team member later has access to a physical iPhone, iOS Camera could be incorporated as an optional extension to the study, providing a useful cross-platform comparison point.

---

## Summary Table

| # | Target                              | Type                  | Platform        |
|---|-------------------------------------|-----------------------|-----------------|
| 1 | Google Lens / Google App            | First-party app       | Android         |
| 2 | QR & Barcode Scanner (TeaCapps)     | Third-party app       | Android         |
| 3 | QR & Barcode Scanner (Gamma Play)   | Third-party app       | Android         |
| 4 | ZXing                               | Open-source lib / app | Android         |
| 5 | ZBar                                | Open-source library   | Cross-platform  |
