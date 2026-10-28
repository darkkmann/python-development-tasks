"""Encrypt and decrypt files with authenticated Fernet encryption."""
from __future__ import annotations

import argparse
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken


def encrypt(source: Path, destination: Path, key_path: Path) -> None:
    key = Fernet.generate_key()
    destination.write_bytes(Fernet(key).encrypt(source.read_bytes()))
    key_path.write_bytes(key)


def decrypt(source: Path, destination: Path, key_path: Path) -> None:
    try:
        plaintext = Fernet(key_path.read_bytes()).decrypt(source.read_bytes())
    except (InvalidToken, ValueError) as error:
        raise RuntimeError("Decryption failed: the key does not match this file.") from error
    destination.write_bytes(plaintext)


def main() -> int:
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a file using Fernet.")
    parser.add_argument("action", choices=("encrypt", "decrypt"))
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--key", type=Path, help="Key-file path; required to decrypt.")
    args = parser.parse_args()
    try:
        if args.action == "encrypt":
            key_path = args.key or args.destination.with_suffix(args.destination.suffix + ".key")
            encrypt(args.source, args.destination, key_path)
            print(f"Encrypted to {args.destination}; keep the key safe at {key_path}.")
        else:
            if args.key is None:
                parser.error("--key is required when decrypting")
            decrypt(args.source, args.destination, args.key)
            print(f"Decrypted to {args.destination}.")
    except (OSError, RuntimeError) as error:
        print(f"Error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
