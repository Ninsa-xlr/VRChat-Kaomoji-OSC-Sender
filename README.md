# VRChat Kaomoji OSC Sender 🌸

A sleek, modern Python desktop application built with `tkinter` and `python-osc` that allows you to instantly transmit a massive collection of kaomojis directly to your VRChat chatbox using OSC (`/chatbox/input`), while simultaneously copying them to your clipboard.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![OSC Enabled](https://img.shields.io/badge/VRChat-OSC-purple.svg)
![Theme](https://img.shields.io/badge/theme-Lila%20Dark-ff77ff.svg)

---

## ✨ Features

* **🎨 Lila Dark Theme:** A cozy, modern dark purple and lavender palette designed to eliminate eye strain during long VRChat sessions.
* **📂 Tiny Catalog Menu:** Instantly switch between different kaomoji categories using a compact, streamlined dropdown menu[cite: 1].
* **🔍 Live Search Bar:** Type any keyword or symbol to search and filter through the entire kaomoji collection in real-time[cite: 1].
* **⚡ Dual Action (OSC + Clipboard):** Clicking any kaomoji button immediately sends it to your VRChat chatbox *and* copies it to your system clipboard for easy pasting anywhere else[cite: 1].
* **🛡️ Crash-Proof Startup:** Built with safe UTF-8 encoding and built-in startup error handling.

---

## 📋 Prerequisites

Make sure you have **Python 3** installed on your system. You will also need the `python-osc` library to handle network communication with VRChat.

Open your terminal or command prompt and run:
```bash
pip install python-osc
