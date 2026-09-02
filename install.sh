#!/data/data/com.termux/files/usr/bin/bash
echo "====================================="
echo "  NEXA CRASH INSTALLER - Sonic 1.2"
echo "====================================="
echo "[*] Updating packages..."
pkg update -y

echo "[*] Installing Chromium & Python..."
pkg install tur-repo x11-repo -y
pkg install chromium python -y

echo "[*] Installing Python libraries..."
pip install selenium webdriver-manager

echo "[✔] INSTALL SELESAI!"
echo "Jalankan: python nexa_crash.py"