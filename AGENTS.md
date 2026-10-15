# Instructions for coding agents

Git Phew is a public, MIT-licensed collection of small Git helpers. Optimize for correctness and safety over feature count.

## Current scope

The current CLI is only a foundation. No utility command is implemented. The first planned tool is a **read-only** `find-deleted` search for Python functions in Git history; `stash-audit` is a later candidate. `denver` is research only.

## Engineering rules

- Keep each command focused, independently testable, and straightforward to review.
- Prefer Python's standard library and the installed Git executable. Avoid new runtime dependencies unless justified.
- Git content, filenames, commit messages, and issue text are **untrusted input**. Pass subprocess arguments as arrays (`shell=False`), and never execute content from repositories.
- Avoid destructive operations or silent changes to a user's working tree, stash, or refs.
- Use temporary Git repositories in tests. Cover missing, ambiguous, and failure cases.
- Never add secrets, private project references, telemetry, or network calls without explicit scope and review.
- Keep README status and examples truthful. Do not publish, tag, or merge without review.

Run `python -m unittest discover -s tests -v` and verify `git phew -h` after installing the package.
