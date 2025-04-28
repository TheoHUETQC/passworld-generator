# 🛠️ BrewKey - Developer Notes

Welcome to the BrewKey development space!  
This document provides technical notes, architecture details, and guidelines for further improving BrewKey across platforms.

---

## 📦 Project Structure Overview
```
📂 password-generator/ 
├── 🧠 main.py → Console version (Python) 
│ 
├── 📂 windows/ 
│    ├── 🪟 WindowsPassWordGenerator.py → Tkinter GUI application 
│    └── 🧪 generateur_mdp23-2.exe → Compiled Windows executable 
│ 
├── 📂 android/ 
│    └── 🤖 generateur_mdp_android.py → Android GUI (in development, Kivy) 
│ 
├── 📂 logo/ 
│    ├── 🖼️ logo.png → App icon 
│    └── 🧊 logo.ico → Executable icon 
│ 
└── 📄 README.md → General user documentation```
```

---

## 🔐 Core Concept

- Deterministic password generation using **SHA-256 hashing**.
- Inputs:
  - **Identifier**: service/site/application name.
  - **Master Password**: single master key known only by the user.
- Outputs:
  - Secure, repeatable password with a default **length of 23 characters**.

> **Important:** No sensitive data is ever saved locally or sent over the network.

---

## ⚙️ Technologies Used

| Platform     | Tech Stack                         |
|--------------|-------------------------------------|
| Console      | Python 3.9+ (hashlib)               |
| Windows GUI  | Python 3.9+, Tkinter                |
| Android GUI  | Python 3.9+, Kivy (Python mobile)   |

---

## 🖥️ Windows Version Notes

- Built using **Tkinter** (native, lightweight GUI library).
- `.exe` compiled using **pyinstaller**:
  ```bash
  pyinstaller --onefile --icon=logo/logo.ico WindowsPassWordGenerator.py
    ```

- Features:

    - Input fields for Identifier and Master Password.

    - Password visibility toggle.

    - Clipboard copy.

    - Basic error handling (empty fields, etc.).

---

## 🔮 Possible Improvements

- Add an option to customize password length.

- Support for different character sets (numbers only, symbols, etc.).

- A better GUI theme (using ttkbootstrap or custom Tkinter themes).

- System tray mode (background app with pop-up generator).

---

## 📱 Android Version Notes (Kivy)

- GUI already functional using Kivy.

- Layout:

    - Simple input fields.

    - "Generate" button.

    - Password visibility toggle.

- Still in development:

    - Clipboard support.

    - APK packaging (buildozer needed).

    - Permissions (Kivy needs access to clipboard, screen management).

---

## 🔮 Possible Improvements

- Implement dark/light mode.

- Allow optional password length setting.

- Support biometric unlock (e.g., fingerprint to autofill master password).

---

## 🧪 Password Generation Logic

Main password generation is based on:

hashlib.sha256((identifier + master_password).encode('utf-8')).hexdigest()

- Resulting hash is converted into an integer.

- Then sliced and mapped onto a customized character set to produce a password.

- The process is entirely deterministic, meaning same input = same password every time.

---

## 🛠️ Development To-Do
Windows

Improve error messages with friendly popups.

Add customizable settings (length, character types).

- Modernize UI.

Android

Finalize basic app structure.

Package an APK using Buildozer.

Optimize screen layout for various device sizes.

- Clipboard integration.

Common

Add optional password hints ("generated for Gmail" visible after creation).

Add a "Password Strength" visual indicator.

- Add localization (English/French) — via simple language files.

---

## 🧠 Best Development Practices

- Minimal dependencies: use standard libraries as much as possible.

- Clear and consistent UI/UX across platforms.

- Security First:

    - Never store master passwords.

    - Always handle input/output securely (masked fields, clipboard auto-clear after X seconds in future versions?).

- Versioning:

    - Keep version numbers in filenames and document them (e.g., generateur_mdp23-2.exe).

---

## ✨ Contributions

- Keep codebase clean and well-commented.

- Propose new features via pull requests or discussions.

- Always focus on simplicity, security, and usability.

---

## 🚀  Brew smarter. Stay safer !