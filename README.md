# Git Phew

**Tiny tools. Big relief.**

Git is powerful. Its little annoyances do not have to be.

Git Phew is an early-stage, open-source collection of small, focused Git helpers. Each tool should solve a real annoyance with a simple command and predictable behavior.

> **Project status:** Foundation only. No utility subcommands have shipped yet; `find-deleted`, `stash-audit`, and `denver` are **not** available.

## Getting started (development)

Requirements: **Python 3.10+** and **Git**.

From a clone of this repository:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
git phew -h
git phew --version
```

Git discovers the installed `git-phew` executable as the `git phew` subcommand. These commands currently show only the CLI foundation.

## Planned tools

| Tool | Goal | Status |
| --- | --- | --- |
| `git phew find-deleted <name>` | Locate previously deleted Python functions in local Git history, without modifying files. | Planned first |
| `git phew stash-audit` | Inspect local stashes without dropping or applying them. | Candidate for later |
| `git phew denver <issue-url>` | Investigate possible fixes for GitHub issues without a linked solution. | Research only |

The roadmap is **not a feature promise**. See [the roadmap](docs/ROADMAP.md).

## Principles

- Solve one well-defined problem at a time; avoid a large framework.
- Default to read-only operations; never silently modify or delete user work.
- Prefer the Python standard library and Git over runtime dependencies.
- Be clear about uncertainty, limitations, and unsupported cases.
- Keep every command independently testable.

## Development

```sh
python -m unittest discover -s tests -v
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

[MIT](LICENSE).
