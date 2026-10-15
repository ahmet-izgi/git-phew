"""Find verifiable Python function removals in local Git history.

This command reads committed Git objects only. It never checks out, restores,
executes, or modifies repository contents. Ambiguous results stay ambiguous.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
import io
import os
from pathlib import Path
import re
import subprocess
import tokenize


class GitHistoryError(Exception):
    """Git or input failure that can be reported without a traceback."""


@dataclass(frozen=True)
class Removal:
    name: str
    path: str
    removed_in: str
    last_present_in: str
    source: str
    line: int


def _git(repo: Path, *args: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise GitHistoryError(f"Could not run Git: {exc}") from exc
    if result.returncode:
        detail = os.fsdecode(result.stderr).strip() or "Git command failed"
        raise GitHistoryError(detail)
    return result.stdout


def _function_nodes(blob: bytes) -> tuple[str, list[ast.AST]] | None:
    try:
        encoding, _ = tokenize.detect_encoding(io.BytesIO(blob).readline)
        source = blob.decode(encoding)
        tree = ast.parse(source)
    except (SyntaxError, UnicodeError, LookupError, tokenize.TokenError):
        return None
    nodes = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    return source, nodes


def _blob(repo: Path, revision: str, path: str) -> bytes:
    # The revisions and paths originate from local Git, not from a shell.
    return _git(repo, "show", f"{revision}:{path}")


def _changes(repo: Path, parent: str, commit: str) -> list[tuple[str, str, str]]:
    data = _git(
        repo, "diff", "--no-ext-diff", "--no-textconv",
        "--name-status", "-z", "-M", parent, commit, "--", "*.py",
    ).split(b"\0")
    changes: list[tuple[str, str, str]] = []
    i = 0
    while i < len(data) and data[i]:
        status = os.fsdecode(data[i])
        i += 1
        if i >= len(data):
            raise GitHistoryError("Unexpected output from git diff")
        previous = os.fsdecode(data[i])
        i += 1
        current = previous
        if status.startswith(("R", "C")):
            if i >= len(data):
                raise GitHistoryError("Unexpected rename output from git diff")
            current = os.fsdecode(data[i])
            i += 1
        changes.append((status, previous, current))
    return changes


def search(
    repo: Path, name: str, *,
    path: str | None = None,
    commit_prefix: str | None = None,
) -> list[Removal]:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        raise GitHistoryError("Function name must be a simple Python identifier")
    if commit_prefix is not None and not re.fullmatch(r"[0-9a-fA-F]{7,40}", commit_prefix):
        raise GitHistoryError("--commit must be a Git commit SHA prefix (7–40 hex digits)")

    root = os.fsdecode(_git(repo, "rev-parse", "--show-toplevel")).rstrip("\n")
    if not root:
        raise GitHistoryError("A non-bare Git working tree is required")
    repo = Path(root)

    # -G preselects commits whose changed lines contain a Python definition.
    # This avoids inspecting every blob in the full repository history.
    expression = r"^[[:space:]]*(async[[:space:]]+)?def[[:space:]]+" + name + r"[[:space:]]*\("
    history = _git(
        repo, "log", "--topo-order", "--no-merges", "--format=%H",
        "--no-ext-diff", "--no-textconv", "--extended-regexp",
        "-G", expression, "HEAD", "--", "*.py",
    ).decode("ascii").splitlines()
    matches: list[Removal] = []

    for sha in history:
        if commit_prefix and not sha.startswith(commit_prefix.lower()):
            continue
        parents = _git(repo, "rev-list", "--parents", "-n", "1", sha).decode("ascii").split()
        if len(parents) != 2:
            continue  # Root commits and merge commits cannot prove this transition.
        parent = parents[1]
        for status, old_path, new_path in _changes(repo, parent, sha):
            if status[0] not in ("M", "D", "R"):
                continue
            if path is not None and path not in (old_path, new_path):
                continue
            before = _function_nodes(_blob(repo, parent, old_path))
            if before is None:
                continue
            before_source, before_nodes = before
            previous_defs = [node for node in before_nodes if node.name == name]
            if len(previous_defs) != 1:
                continue  # Do not guess among definitions with identical names.

            if status.startswith("D"):
                after_nodes: list[ast.AST] = []
            else:
                after = _function_nodes(_blob(repo, sha, new_path))
                if after is None:
                    continue  # Unknown parse state is not proof of removal.
                _, after_nodes = after
            if any(node.name == name for node in after_nodes):
                continue

            node = previous_defs[0]
            begin = min([node.lineno] + [decorator.lineno for decorator in node.decorator_list])
            if node.end_lineno is None:
                continue
            snippet = "".join(before_source.splitlines(keepends=True)[begin - 1:node.end_lineno])
            matches.append(Removal(name, old_path, sha, parent, snippet, begin))
    return matches
