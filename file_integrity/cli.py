"""User-facing CLI with stable exit codes: 0 OK, 1 mismatch, 2 error."""

import argparse
import sys
from collections.abc import Sequence

from .hashing import sha256_file
from .verification import verify_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="file-integrity",
        description="Compute and verify SHA-256 hashes of local files.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    hash_command = commands.add_parser("hash", help="print a file's SHA-256 digest")
    hash_command.add_argument("file", help="path to the file")
    verify_command = commands.add_parser("verify", help="compare a file with an expected SHA-256 digest")
    verify_command.add_argument("file", help="path to the file")
    verify_command.add_argument("sha256", help="trusted 64-character hex SHA-256 digest")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "hash":
            print(sha256_file(args.file))
            return 0
        if verify_file(args.file, args.sha256):
            print("OK: SHA-256 matches")
            return 0
        print("MISMATCH: SHA-256 does not match", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
