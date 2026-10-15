"""Allow `python -m git_phew` for local smoke testing."""

from .cli import main

raise SystemExit(main())
