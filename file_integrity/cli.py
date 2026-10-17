"""User-facing CLI with stable exit codes: 0 OK, 1 mismatch, 2 error."""

import argparse
import json
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
    hash_command.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON output",
    )

    verify_command = commands.add_parser(
        "verify", help="compare a file with an expected SHA-256 digest",
    )
    verify_command.add_argument("file", help="path to the file")
    verify_command.add_argument("sha256", help="trusted 64-character hex SHA-256 digest")
    verify_command.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON output",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "hash":
            digest = sha256_file(args.file)
            if args.json:
                print(json.dumps({"file": args.file, "sha256": digest}))
            else:
                print(digest)
            return 0

        matches = verify_file(args.file, args.sha256)
        if args.json:
            print(json.dumps({
                "file": args.file,
                "expected_sha256": args.sha256.lower(),
                "matches": matches,
            }))
        elif matches:
            print("OK: SHA-256 matches")
        else:
            print("MISMATCH: SHA-256 does not match", file=sys.stderr)
        return 0 if matches else 1
    except (OSError, ValueError) as error:
        if args.json:
            print(json.dumps({"error": str(error)}))
        else:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
