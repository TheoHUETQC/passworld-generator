# Deterministic Password Generator - Windows

This project is a **password generator** application developed using **Python** and **Tkinter**. It generates secure passwords deterministically based on a user-provided identifier and a master password.

---

## Features

- **Deterministic Password Generation**:
  Passwords are generated using a secure hashing algorithm to ensure consistent results for the same inputs.
- **Modern User Interface**:
  A clean and intuitive GUI built with Tkinter.
- **Masked Password Display**:
  Hide or show the generated password for added security.
- **Clipboard Copy**:
  Copy the generated password to the clipboard with one click.
- **Real-time Feedback**:
  Enables the "Generate" button when inputs are modified.

---

## How It Works

The application uses the **SHA-256** hashing algorithm to process the provided identifier and master password, generating a unique and secure password of 23 characters.

### Example Flow

1. Enter an identifier and a master password.
2. Click the "Generate Password" button.
3. The app displays a masked password and enables options to copy or reveal the password.

---

## Prerequisites

- **Python 3.9+** must be installed.
- Required Python libraries: `tkinter`, `hashlib`.
