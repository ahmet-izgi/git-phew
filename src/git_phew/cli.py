"""Minimal, conservative command-line entry point for Git Phew."""

from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import sys
import unicodedata
from typing import Sequence

from .commands.find_deleted import GitHistoryError, search


def _installed_version() -> str:
    try:
        return version("git-phew")
    except PackageNotFoundError:
        return "development"


def _is_control(char: str) -> bool:
    if char in ("\n", "\r", "\t"):
        return True
    category = unicodedata.category(char)
    return category.startswith("C") or category in ("Zl", "Zp")


def _sanitize(
    text: str, *, allow_newlines: bool = False, allow_tabs: bool = False
) -> str:
    result: list[str] = []
    if allow_newlines:
        text = text.replace("\r\n", "\n")
    for char in text:
        if allow_newlines and char == "\n":
            result.append(char)
        elif allow_tabs and char == "\t":
            result.append(char)
        elif char == "\n":
            result.append("\\n")
        elif char == "\r":
            result.append("\\r")
        elif char == "\t":
            result.append("\\t")
        elif not _is_control(char):
            result.append(char)
        else:
            code = ord(char)
            if code <= 0xFF:
                result.append(f"\\x{code:02x}")
            elif code <= 0xFFFF:
                result.append(f"\\u{code:04x}")
            else:
                result.append(f"\\U{code:08x}")
    return "".join(result)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="git phew",
        description="Tiny tools. Big relief.",
    )
    parser.add_argument(
        "--version", action="version", version=f"git-phew {_installed_version()}",
    )
    commands = parser.add_subparsers(dest="command")
    deleted = commands.add_parser(
        "find-deleted", help="Find verified removals of Python functions in Git history",
    )
    deleted.add_argument("name", help="Python function name")
    deleted.add_argument(
        "--path", help="Exact repository-relative file path, for disambiguation",
    )
    deleted.add_argument(
        "--commit", help="Full removal commit SHA or unique SHA prefix",
    )
    deleted.add_argument(
        "--repo", type=Path, default=Path.cwd(), metavar="DIRECTORY",
        help="Working tree to inspect (default: current directory)",
    )
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0
    if args.command == "find-deleted":
        try:
            matches = search(
                args.repo, args.name, path=args.path, commit_prefix=args.commit,
            )
        except GitHistoryError as exc:
            print(f"git phew: {_sanitize(str(exc), allow_newlines=True)}", file=sys.stderr)
            return 2
        if not matches:
            print(
                f"No verified removal of {args.name!r} found in non-merge "
                "commits reachable from HEAD."
            )
            return 1
        if len(matches) > 1:
            print(f"Found {len(matches)} removals; refusing to choose one:")
            for match in matches[:20]:
                print(f"  {match.removed_in[:12]}  {_sanitize(match.path)}:{match.line}")
            if len(matches) > 20:
                print(f"  ... and {len(matches) - 20} more")
            print("Narrow the search with --path and/or --commit.")
            return 3

        match = matches[0]
        print(f"Removed from: {_sanitize(match.path)}:{match.line}")
        print(f"Removal commit: {match.removed_in}")
        print(f"Last present in: {match.last_present_in}")
        print(
            "Note: This proves removal from that file, not that the "
            "function is absent from all later code."
        )
        safe_source = _sanitize(match.source, allow_newlines=True, allow_tabs=True)
        print("\n" + safe_source, end="" if safe_source.endswith("\n") else "\n")
        return 0
    parser.error("Unsupported command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
