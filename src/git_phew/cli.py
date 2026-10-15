"""Minimal command-line entry point for Git Phew."""

from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version
from typing import Sequence


def _installed_version() -> str:
    try:
        return version("git-phew")
    except PackageNotFoundError:
        return "development"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="git phew",
        description="Tiny tools. Big relief.",
        epilog="Utility commands are not available yet.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"git-phew {_installed_version()}",
    )
    parser.parse_args(argv)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
