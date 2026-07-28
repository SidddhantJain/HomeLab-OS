# Building the Windows Remote Installation Assistant

This guide describes how to build and package the Windows installer assistant executable.

---

## ⚙️ Prerequisites for Packaging

- Node.js 20+ / Electron or PyInstaller (Python desktop wrapper)
- Inno Setup 6.0+ (Windows installer compiler)

---

## 🛠️ Package Compilation Steps

### 1. Build Desktop Application Bundle
```powershell
# Navigate to installer UI directory
cd installer/windows/src

# Install dependencies
npm install

# Package Electron / Executable bundle
npm run package:win
```

### 2. Compile Windows Installer Setup Executable
Using Inno Setup Compiler:
1. Open `installer/windows/setup_script.iss` in Inno Setup.
2. Click **Compile** to generate `HomeLabOS_Setup_v1.0.exe` in `release/packages/`.

---

## 📦 Output Artifacts

- `release/packages/HomeLabOS_Remote_Setup_v1.0.0.exe` (Windows Installer Wizard)
