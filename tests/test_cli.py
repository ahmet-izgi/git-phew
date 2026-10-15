"""Smoke tests for the Git Phew CLI."""

import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from git_phew.cli import _sanitize, main


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

    def test_sanitize_escapes_control_characters_and_preserves_unicode(self) -> None:
        raw = "path/\x1b[31;1m\a\b\r\nçşğüöıİ.py"
        sanitized = _sanitize(raw)
        self.assertNotIn("\x1b", sanitized)
        self.assertNotIn("\a", sanitized)
        self.assertNotIn("\b", sanitized)
        self.assertNotIn("\r", sanitized)
        self.assertNotIn("\n", sanitized)
        self.assertIn(r"\x1b[31;1m", sanitized)
        self.assertIn(r"\x07", sanitized)
        self.assertIn(r"\x08", sanitized)
        self.assertIn(r"\r", sanitized)
        self.assertIn(r"\n", sanitized)
        self.assertIn("çşğüöıİ.py", sanitized)

    def test_sanitize_source_preserves_multiline_and_tabs(self) -> None:
        source = "def func():\n\t# yorum: Türkçe\n\treturn '\x1b[2J'\n"
        sanitized = _sanitize(source, allow_newlines=True, allow_tabs=True)
        self.assertNotIn("\x1b", sanitized)
        self.assertIn(r"\x1b[2J", sanitized)
        self.assertIn("\n\t# yorum: Türkçe\n\treturn ", sanitized)

    def test_sanitize_normalizes_crlf_and_escapes_isolated_cr(self) -> None:
        crlf_source = "def ok():\r\n    return 1\r\ndef evil():\r\n    pass\r\n"
        sanitized = _sanitize(crlf_source, allow_newlines=True, allow_tabs=True)
        self.assertNotIn("\r\n", sanitized)
        self.assertIn("def ok():\n    return 1\n", sanitized)

        isolated_cr = "def safe():\rdef evil():\n    pass\n"
        sanitized_isolated = _sanitize(isolated_cr, allow_newlines=True, allow_tabs=True)
        self.assertIn(r"\r", sanitized_isolated)
        self.assertNotIn("\rdef evil", sanitized_isolated)


if __name__ == "__main__":
    unittest.main()
