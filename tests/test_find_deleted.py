"""Integration tests using disposable local Git histories."""

from contextlib import redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from git_phew.cli import main
from git_phew.commands.find_deleted import GitHistoryError, search


class FindDeletedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        self.git("init", "-q")

    def git(self, *args: str) -> str:
        env = os.environ.copy()
        env.update({
            "GIT_AUTHOR_NAME": "Git Phew Test",
            "GIT_AUTHOR_EMAIL": "git-phew-test@example.invalid",
            "GIT_COMMITTER_NAME": "Git Phew Test",
            "GIT_COMMITTER_EMAIL": "git-phew-test@example.invalid",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
        })
        result = subprocess.run(
            ["git", "-C", str(self.repo), "-c", "commit.gpgsign=false", *args],
            capture_output=True, text=True, check=True, env=env,
        )
        return result.stdout.strip()

    def write(self, path: str, content: str) -> None:
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def run_cli(self, *args: str) -> tuple[int, str, str]:
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            status = main(["find-deleted", *args, "--repo", str(self.repo)])
        return status, output.getvalue(), errors.getvalue()

    def test_find_function_removed_from_file(self) -> None:
        self.write("src/helpers.py", "def calculate_fee(x):\n    return x * 2\n")
        previous = self.commit("add function")
        self.write("src/helpers.py", "PRICE = 2\n")
        removed = self.commit("remove function")
        status, output, errors = self.run_cli("calculate_fee")
        self.assertEqual((status, errors), (0, ""))
        self.assertIn("return x * 2", output)
        self.assertIn(previous, output)
        self.assertIn(removed, output)
        self.assertIn("src/helpers.py", output)

    def test_file_deletion_is_detected(self) -> None:
        self.write("old.py", "def lost():\n    return 42\n")
        self.commit("add old")
        (self.repo / "old.py").unlink()
        self.commit("delete old")
        self.assertEqual(self.run_cli("lost")[0], 0)

    def test_signature_change_is_not_a_removal(self) -> None:
        self.write("module.py", "def keep(x):\n    return x\n")
        self.commit("add")
        self.write("module.py", "def keep(x, y):\n    return x + y\n")
        self.commit("update signature")
        self.assertEqual(self.run_cli("keep")[0], 1)

    def test_git_rename_preserving_function_is_not_a_removal(self) -> None:
        self.write("old.py", "def stay():\n    return 1\n")
        self.commit("add")
        self.git("mv", "old.py", "moved.py")
        self.commit("rename")
        self.assertEqual(self.run_cli("stay")[0], 1)

    def test_multiple_removals_require_disambiguation(self) -> None:
        for filename in ("one.py", "two.py"):
            self.write(filename, "def same():\n    return 1\n")
        self.commit("add")
        for filename in ("one.py", "two.py"):
            self.write(filename, "VALUE = 1\n")
        removal_sha = self.commit("remove")
        status, output, _ = self.run_cli("same")
        self.assertEqual(status, 3)
        self.assertIn("refusing to choose", output)
        status, output, _ = self.run_cli("same", "--path", "one.py")
        self.assertEqual(status, 0)
        self.assertIn("one.py", output)
        status, _, _ = self.run_cli("same", "--commit", removal_sha[:12])
        self.assertEqual(status, 3)

    def test_decorated_async_function_source_is_preserved(self) -> None:
        self.write("mod.py", "@decorator\nasync def fetch():\n    return 5\n")
        self.commit("add async function")
        self.write("mod.py", "pass\n")
        self.commit("remove async function")
        status, output, _ = self.run_cli("fetch")
        self.assertEqual(status, 0)
        self.assertIn("@decorator\nasync def fetch():", output)

    def test_dirty_worktree_is_not_modified(self) -> None:
        self.write("mod.py", "def disappeared():\n    return 1\n")
        self.commit("add")
        self.write("mod.py", "value = 2\n")
        self.commit("remove")
        self.write("mod.py", "value = 3\n# unpublished work\n")
        original_status = self.git("status", "--porcelain")
        status, _, _ = self.run_cli("disappeared")
        self.assertEqual(status, 0)
        self.assertEqual(self.git("status", "--porcelain"), original_status)
        self.assertIn("# unpublished work", (self.repo / "mod.py").read_text())

    def test_unparseable_after_state_is_not_assumed_deleted(self) -> None:
        self.write("mod.py", "def uncertain():\n    return 1\n")
        self.commit("add")
        self.write("mod.py", "def broken(\n")
        self.commit("invalid Python")
        self.assertEqual(self.run_cli("uncertain")[0], 1)

    def test_invalid_function_name_is_rejected(self) -> None:
        status, _, errors = self.run_cli("foo; touch malicious")
        self.assertEqual(status, 2)
        self.assertIn("simple Python identifier", errors)

    def test_empty_repo_returns_readable_git_error(self) -> None:
        status, _, errors = self.run_cli("anything")
        self.assertEqual(status, 2)
        self.assertIn("HEAD", errors)

    def test_duplicate_definitions_in_one_file_are_skipped(self) -> None:
        self.write(
            "mod.py",
            "class A:\n    def duplicate(self):\n        pass\n"
            "class B:\n    def duplicate(self):\n        pass\n",
        )
        self.commit("add")
        self.write("mod.py", "pass\n")
        self.commit("remove")
        self.assertEqual(self.run_cli("duplicate")[0], 1)


if __name__ == "__main__":
    unittest.main()
