#!/usr/bin/env python3
"""envtrace - trace environment variable usage across a codebase."""
import argparse
import sys
from pathlib import Path

from scanner import scan_directory, parse_dotenv
from reporter import report


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="envtrace",
        description="Trace environment variable usage across a codebase.",
    )
    parser.add_argument("path", nargs="?", default=".", help="directory to scan")
    parser.add_argument("--env", help="path to .env file to compare against")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument(
        "--ignore", action="append", default=[], help="directory names to ignore"
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    used = scan_directory(root, args.ignore)

    documented = set()
    if args.env:
        documented = parse_dotenv(Path(args.env).resolve())
    else:
        for candidate in (".env", ".env.example", ".env.sample", ".env.template"):
            p = root / candidate
            if p.is_file():
                documented = parse_dotenv(p)
                break

    report(used, documented, args.format)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())