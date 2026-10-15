"""Minimal, conservative command-line entry point for Git Phew."""

from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import sys
from typing import Sequence

from .commands.find_deleted import GitHistoryError, search


def _installed_version() -> str:
    try:
        return version("git-phew")
    except PackageNotFoundError:
        return "development"


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
            print(f"git phew: {exc}", file=sys.stderr)
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
                print(f"  {match.removed_in[:12]}  {match.path}:{match.line}")
            if len(matches) > 20:
                print(f"  ... and {len(matches) - 20} more")
            print("Narrow the search with --path and/or --commit.")
            return 3

        match = matches[0]
        print(f"Removed from: {match.path}:{match.line}")
        print(f"Removal commit: {match.removed_in}")
        print(f"Last present in: {match.last_present_in}")
        print(
            "Note: This proves removal from that file, not that the "
            "function is absent from all later code."
        )
        print("\n" + match.source, end="" if match.source.endswith("\n") else "\n")
        return 0
    parser.error("Unsupported command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
