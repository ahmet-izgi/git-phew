"""Smoke tests for the Git Phew CLI."""

import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from git_phew.cli import main


class CLITests(unittest.TestCase):
    def test_no_arguments_shows_help(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main([]), 0)
        self.assertIn("git phew", output.getvalue())
        self.assertIn("find-deleted", output.getvalue())

    def test_version_flag(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output), self.assertRaises(SystemExit) as exit:
            main(["--version"])
        self.assertEqual(exit.exception.code, 0)
        self.assertIn("git-phew ", output.getvalue())

    def test_unknown_command_fails_closed(self) -> None:
        errors = io.StringIO()
        with redirect_stderr(errors), self.assertRaises(SystemExit) as exit:
            main(["not-a-command"])
        self.assertEqual(exit.exception.code, 2)
        self.assertIn("invalid choice", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
