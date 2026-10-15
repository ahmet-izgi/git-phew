# Git Phew

**Tiny tools. Big relief.**

Git is powerful. Its little annoyances do not have to be.

Git Phew is an early-stage, open-source collection of small, focused Git helpers. Each tool should solve a real annoyance with a simple command and predictable behavior.

> **Project status:** Early development. The first utility, \`find-deleted\`, is being developed and tested; no stable release has been published.

## Getting started (development)

Requirements: **Python 3.10+** and **Git**.

From a clone of this repository:

\`\`\`sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
git phew -h
git phew --version
\`\`\`

### Find a historical Python function removal

\`\`\`sh
git phew find-deleted calculate_fee
git phew find-deleted calculate_fee --path src/payments.py
git phew find-deleted calculate_fee --commit 1234567
\`\`\`

This command reads **committed, local Git history reachable from HEAD** and searches non-merge commits for evidence that a named Python function was removed from a file. It reports the removal commit, previous commit, path, and original source. It **does not** restore files, use your clipboard, run repository code, or contact a network service.

For safety, multiple candidate removals are **not** automatically ranked; specify an exact \`--path\` and/or a removal \`--commit\` prefix to narrow the result. A removal from a file is **not proof** the function does not exist somewhere else today.

**Deliberate limitations:** Python functions only; ASCII identifier names; inspectable Python source compatible with the running interpreter; current HEAD history only; merge commits excluded. Files with syntax errors or multiple definitions of the same name are skipped instead of guessed. Function moves across files or unusual Git histories may require manual investigation.

Exit codes: \`0\` one verified result, \`1\` no verified removal, \`2\` invalid input/Git error, \`3\` ambiguous results. Worktree and refs remain untouched.

## Planned tools

| Tool | Goal | Status |
| --- | --- | --- |
| \`git phew find-deleted <name>\` | Locate historical Python function removals without modifying files. | Experimental; no release |
| \`git phew stash-audit\` | Inspect local stashes without dropping or applying them. | Candidate for later |
| \`git phew denver <issue-url>\` | Investigate possible fixes for GitHub issues without a linked solution. | Research only |

The roadmap is **not a feature promise**. See [the roadmap](docs/ROADMAP.md).

## Principles

- Solve one well-defined problem at a time; avoid a large framework.
- Default to read-only operations; never silently modify or delete user work.
- Prefer the Python standard library and Git over runtime dependencies.
- Be clear about uncertainty, limitations, and unsupported cases.
- Keep every command independently testable.

## Development

\`\`\`sh
python -m unittest discover -s tests -v
\`\`\`

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

[MIT](LICENSE).
