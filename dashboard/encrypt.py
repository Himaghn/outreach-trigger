"""Encrypt the dashboard data with the DASHBOARD_PASSWORD secret.

    python dashboard/encrypt.py data.json _site/data.json

AES-256-GCM with a key derived from the password (PBKDF2-SHA256, 600,000 rounds).
The salt is fixed for this site so a browser can remember the derived key (not the
password) between visits; the IV is fresh for every build. Only the encrypted file is published; the page decrypts it in the
browser after you type the password. Refuses to run without a password, so the
plain data can never be published by mistake.
"""
import base64
import json
import os
import sys

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 600_000
SALT = b"prof-outreach-dashboard/v1"


def main(src: str, dst: str) -> int:
    password = os.environ.get("DASHBOARD_PASSWORD", "")
    if len(password) < 8:
        print("DASHBOARD_PASSWORD is missing or shorter than 8 characters - not publishing.")
        return 1
    plain = open(src, "rb").read()
    salt, iv = SALT, os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS).derive(password.encode())
    ct = AESGCM(key).encrypt(iv, plain, None)  # ciphertext followed by the 16-byte tag, as WebCrypto expects
    b64 = lambda b: base64.b64encode(b).decode()
    with open(dst, "w") as f:
        json.dump({"v": 1, "kdf": "PBKDF2-SHA256", "iterations": ITERATIONS,
                   "salt": b64(salt), "iv": b64(iv), "data": b64(ct)}, f)
    print(f"Encrypted dashboard data written ({len(ct)} bytes).")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
