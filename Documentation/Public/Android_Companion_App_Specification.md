# HomeLab OS — Android Native Companion & Touch IDE Specification

> Technical architectural specification for the **HomeLab OS Android Native Mobile & Tablet Application** (`.apk` / `.aab`) featuring biometric authentication, real-time push alerts, client SHA-256 media auto-upload, low-latency WebRTC P2P remote terminal, and Jetpack Compose Touch-Optimized IDE interface.

---

## 📱 Architectural Overview & Feature Stack

1. **Biometric Authentication & Hardware Protection**:
   - Native Android `BiometricPrompt` API integration supporting Fingerprint, Face Unlock, and Hardware Security Module (HSM) stored zero-trust tokens.
2. **Real-Time Push Alerts (FCM)**:
   - Firebase Cloud Messaging (FCM) push pipeline rendering prioritized alerts (*Info*, *Warning*, *Critical*, *Emergency SMART Disk Alert*).
3. **Jetpack Compose Touch-Optimized Developer Keyboard**:
   - Floating action bar delivering developer keys (`Ctrl`, `Alt`, `Esc`, `Tab`, `|`, `->`, `<-`, `{`, `}`, `[`, `]`, `$`).
   - 1-Click remote compilation button triggering tariff-aware build farm compilation.
   - Split-screen touch code editor & live WebRTC terminal.
4. **Camera Media Auto-Backup & Deduplication**:
   - Background camera media auto-upload with client-side SHA-256 hash deduplication to prevent duplicate server file transfers.

---

## ⚙️ Building the Android App

To build the standalone `.apk` and `.aab` bundles:
```bash
python scripts/build_android_app.py
```
Output binaries are generated in `release/android/HomeLabOS-Companion-v5.0.0.apk` and `.aab`.
