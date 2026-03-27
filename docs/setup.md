# Setup Guide — QR Code Scanner Security Study

This guide walks through the full environment setup for our black-box security study of Android QR code scanner applications. It covers installing the required tools on macOS, creating an Android emulator, routing traffic through mitmproxy, and capturing HTTPS traffic for analysis.

---

## Prerequisites

Before starting, make sure you have the following:

- A Mac running macOS (Apple Silicon or Intel)
- [Android Studio](https://developer.android.com/studio) installed
- Homebrew installed (`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`)
- Admin access to your machine
- Basic familiarity with the terminal

---

## 1. Android Studio and Emulator Setup

### Install Android Studio

Download and install [Android Studio](https://developer.android.com/studio). Follow the standard installation wizard and allow it to download the default SDK components.

### Create a Pixel 6 Emulator

1. Open Android Studio.
2. Go to **Tools > Device Manager**.
3. Click **Create Device**.
4. Select **Phone > Pixel 6** and click **Next**.
5. Choose a system image — select one with **Google APIs** (not Google Play, since Play Store images restrict proxy cert installation).
6. Click **Finish** to create the AVD.

### Start the Emulator

Launch the Pixel 6 AVD from Device Manager. Wait for it to fully boot before proceeding.

---

## 2. mitmproxy Setup

### Install mitmproxy

```bash
brew install mitmproxy
```

### Start mitmproxy

In a terminal window, run:

```bash
mitmproxy --ssl-insecure
```

> **Why `--ssl-insecure`?** In our environment, HTTPS interception initially failed due to certificate verification issues on certain app traffic. Running with `--ssl-insecure` bypasses upstream SSL verification and allowed reliable HTTPS interception. Leave this flag in place for the duration of testing.

mitmproxy will start listening on port `8080` by default. Keep this terminal window open throughout your session.

---

## 3. Configure the Emulator to Use mitmproxy

The Android emulator uses `10.0.2.2` to reach the Mac host machine. We set the emulator's Wi-Fi proxy to point to mitmproxy running on the host.

1. In the emulator, open **Settings > Network & Internet > Internet**.
2. Long-press **AndroidWifi** and select **Modify network**.
3. Expand **Advanced options**.
4. Set **Proxy** to **Manual**.
5. Enter the following:
   - **Proxy hostname:** `10.0.2.2`
   - **Proxy port:** `8080`
6. Tap **Save**.

All HTTP/HTTPS traffic from the emulator will now be routed through mitmproxy.

---

## 4. Install the mitmproxy CA Certificate on Android

To intercept HTTPS traffic, the emulator must trust the mitmproxy certificate authority.

### Download the Certificate

With the proxy configured and mitmproxy running, open the browser in the emulator and navigate to:

```
http://mitm.it
```

Tap **Android** to download the mitmproxy certificate file (`.pem`).

> If the page does not load, double-check that the proxy settings in step 3 are saved correctly and that mitmproxy is running.

### Install the Certificate

1. Open **Settings > Security > More security settings > Encryption & credentials**.
2. Tap **Install a certificate**.
3. Select **CA certificate**.
4. Android will warn that this allows monitoring of network traffic — tap **Install anyway**.
5. Browse to the downloaded `.pem` file and select it.

### Verify the Certificate Is Installed

1. Go to **Settings > Security > More security settings > Encryption & credentials**.
2. Tap **Trusted credentials**.
3. Switch to the **User** tab.
4. You should see **mitmproxy** listed there.

> The certificate is installed in the **User** trust store, not the System store. This is expected and sufficient for browser-level interception. Some apps that enforce system-level certificate pinning may not be interceptable without additional steps (out of scope for this study).

---

## 5. Wireshark Setup

### Install Wireshark

```bash
brew install --cask wireshark
```

Alternatively, download it from [wireshark.org](https://www.wireshark.org/download.html).

### Capture Traffic

1. Open Wireshark.
2. Select the network interface your Mac is actively using (e.g., `en0` for Wi-Fi, `lo0` for loopback).
3. To filter only the proxy traffic, use the display filter:
   ```
   tcp.port == 8080
   ```
4. Start capture before launching the QR scanner app under test.

> Wireshark gives a low-level view of packets. mitmproxy is better for reading decrypted HTTP/HTTPS request and response content. Use both tools together for a complete picture.

---

## 6. Verification

Once everything is set up, confirm the environment is working correctly:

1. In the emulator browser, navigate to `https://example.com`.
2. The page should load successfully in the browser.
3. Switch to the mitmproxy terminal — you should see the `GET https://example.com/` request listed with a `200` response.

If both of these are true, HTTPS interception is working and you are ready to begin testing QR scanner apps.

---

## 7. Troubleshooting

### Port 8080 is already in use

If mitmproxy fails to start with a port binding error, find and stop the process using that port:

```bash
lsof -i :8080
kill -9 <PID>
```

Then restart mitmproxy.

---

### HTTPS traffic shows `502 Bad Gateway`

This usually means mitmproxy cannot complete the upstream TLS handshake. Make sure you are running:

```bash
mitmproxy --ssl-insecure
```

Without `--ssl-insecure`, certain apps or sites will cause upstream verification failures that result in a 502 error in the proxy log.

---

### Certificate downloaded but Android says it must be installed in Settings

Android does not allow direct installation of CA certificates from the Downloads app. When prompted, do not tap "Open" from the download notification. Instead:

1. Go to **Settings > Security > Encryption & credentials > Install a certificate > CA certificate**.
2. Manually browse to the downloaded file from within that menu.

---

### Magnification shortcut accidentally enabled in the emulator

If the emulator screen suddenly zooms in when you tap, the accessibility magnification shortcut has been triggered (usually by triple-tapping). To disable it:

1. Go to **Settings > Accessibility > Magnification**.
2. Turn off **Magnification shortcut**.

---

### Should I install the mitmproxy certificate on macOS instead of Android?

No. Installing the certificate on macOS would make your Mac trust mitmproxy as a CA — it would have no effect on the Android emulator's trust store. The certificate must be installed **on the Android emulator** so that apps running inside the emulator accept mitmproxy's intercepted TLS connections. The two trust stores are completely separate.
