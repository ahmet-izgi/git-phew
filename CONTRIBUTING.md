# Contributing to Git Phew

Thanks for your interest! Git Phew is intentionally small.

## Before proposing a command

Explain the recurring Git problem, show the existing workaround, and describe how one short command would improve it. Prefer evidence from a real repository or a reproducible example. A new command is not accepted just because it is easy to implement.

## Development

Use Python 3.10+ and Git:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
git phew -h
```

Open a focused pull request with tests and a short explanation of limitations. Use temporary Git repositories for tests of Git behavior, not developers' real working repositories.

## Safety and scope

- Default to read-only behavior. Never silently alter branches, stashes, refs, or working files.
- Handle ambiguous results explicitly; do not guess or claim certainty without evidence.
- Do not add network access, AI APIs, telemetry, or third-party runtime dependencies without a clear, reviewed need.
- Never commit credentials, personal data, local `.env` files, or private repository contents.
- Keep project documentation accurate: do not advertise unreleased features.
