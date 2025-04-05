# 🔐 Deterministic Password Generator

This project is a **deterministic password generator** written in **Python**, offering both a simple **console version** and modern **graphical user interfaces** for **Windows** and **Android** platforms.

It uses secure hashing (SHA-256) to generate repeatable, strong passwords from a unique **identifier** and a **master password**. This approach ensures you always get the same password for the same inputs—without needing to store anything.

---

## ⚙️ Features

- 🔐 **Deterministic password generation** using SHA-256
- 💾 **No data storage** – everything is generated on the fly
- 🖥️ **Windows GUI App** (.exe included)
- 🤖 **Android GUI App** (under development)
- 🧰 **Console version** for quick use or integration
- 📋 **Copy to clipboard** support in GUI versions
- 🧪 **Masked display** of passwords for privacy
- 🆕 **Version system** for releases (e.g., `23-2` = 23-char, version 2)

---

## 📁 Project Structure

``` bash
📂 password-generator/ 
├── 📄 README.md ← This file 
├── 🧠 main.py ← Console version (basic generator) 
│ 
├── 📂 windows/ 
│   ├── 🪟 WindowsPassWordGenerator.py ← GUI source code (Tkinter) 
│   └── 🧪 generateur_mdp23-2.exe ← Compiled Windows app (v2, 23 chars) 
│ 
├── 📂 android/ 
│   └── 🤖 generateur_mdp_android.py ← GUI version for Android (in progress) 
│ 
├── 📂 logo/ 
│   ├── 🖼️ logo.png ← App icon (PNG) 
│   └── 🧊 logo.ico ← App icon for .exe (ICO)
```

---

## 🚀 Quick Usage

### ▶️ 1. Console Version

Run in a terminal with Python 3:

```bash
python main.py
```

You'll be asked for:

- An **identifier** (e.g., "gmail")
- A **master password**

    → You'll get a **deterministically generated password** (23 characters by default).

---

### 🪟 2. Windows App (GUI)

Just launch:

```bash
windows/generateur_mdp23-2.exe
```
- Clean graphical interface
- Clipboard support
- Password visibility toggle
- Built-in error handling

---

### 🤖 3. Android App

The Android version is still under development.
- GUI already functional in android/generateur_mdp_android.py
- Will follow same versioning system as Windows (generateur_mdp23-2)

---

## 🧪 Behind the Scenes

- Passwords are generated using:
```bash
hashlib.sha256((identifier + master_password).encode()).hexdigest()
```
- Then, the output hash is trimmed/encoded to 23 characters using a deterministic slicing strategy, ensuring high entropy.
- The same inputs will **always return the same password**, enabling password retrieval **without storage**.

---

## ✅ Requirements

- **Python 3.9+**
- Standard libraries only: hashlib, tkinter (for GUI versions)

For GUI development:
```bash
pip install pillow
```

---

## 📦 Versioning

The naming follows this logic:

-generateur_mdp23-2.exe

    → Generates 23-character passwords
    → Version 2 of the app

Future versions (with different lengths or improvements) will follow this convention.

---

## 🤝 Contributions & Ideas

Feel free to:

- Suggest features
- Report issues
- Submit pull requests

---

## 🔐 Your Passwords Stay Yours

No network connection is required.

No password is stored anywhere.

Everything happens locally, and deterministically.

---

## 🚀 Stay secure, stay simple!
