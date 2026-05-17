#!/bin/bash

echo " =============================================================================="
echo " AbsoluteSolver: PBKDF2-AES Decryptor - Pre-Use Setup, by chrisrich4892"
echo " =============================================================================="

echo "=== Setting up AbsoluteSolver for first-time use! ==="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 could not be found. Please install Python 3 and try again."
    exit 1
fi

# Ensure pip is installed for Python 3
if ! command -v pip3 &> /dev/null; then
    echo "[*] pip3 not found. Attempting to install package manager dependencies..."
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3-pip
    elif command -v brew &> /dev/null; then
        brew install python
    else
        echo "[!] Could not automatically install pip. Please install python3-pip manually."
        exit 1
    fi
fi

echo "[*] Upgrading pip to the latest version..."
python3 -m pip install --upgrade pip --user &> /dev/null

echo "[*] Installing required decryptor dependencies..."
# pycryptodome provides the required Crypto.Protocol, Crypto.Hash, and Crypto.Cipher modules
python3 -m pip install pycryptodome --user

if [ $? -eq 0 ]; then
    echo -e "- AbsoluteSolver Setup Complete! -"
    echo "You can now run it using: python3 solver.py"
else
    echo -e ":( AbsoluteSolver Setup Failed, Please check your internet connection and permissions."
    exit 1
fi
