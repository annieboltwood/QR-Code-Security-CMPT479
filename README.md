
# QR Code Scanner Security Study
**CMPT 479 — Simon Fraser University**

## Overview
Black-box security testing of QR code scanner apps and libraries.
We test whether scanners warn users about malicious URLs, auto-open links,
leak data to third parties, and properly validate encoded content.

## Team
- Jedidiah Akinola
- Annie Boltwood
- Mahim Chaudhary

## Repository Structure
- `payloads/` — generated QR code images and manifest
- `tools/` — scripts for payload generation and traffic analysis
- `data/` — scan results, network captures, and screenshots
- `docs/` — setup guides and testing logs
- `paper/` — final report
```
qr-security-study/
├── payloads/
├── tools/
├── data/
│   ├── captures/
│   └── screenshots/
├── docs/
├── paper/
├── .gitignore
└── README.md
```

## Setup
See `docs/setup.md` for instructions on configuring mitmproxy and Wireshark.

## Target Apps
See `docs/targets.md` for the list of apps and libraries we tested.
```

