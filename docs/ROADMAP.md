# Roadmap (proposals, not commitments)

Git Phew will grow only when a narrowly scoped utility demonstrates a real benefit. The repository is currently a CLI foundation, not a collection of working utilities.

## First: `find-deleted`

Start with **Python functions only**. Search reachable local Git history and show a candidate's source, file path, and commit reference without modifying the repository. Handle duplicate names, renamed files, and missing results conservatively. Verify behavior against disposable repositories with controlled commits before making product claims.

## Later candidate: `stash-audit`

Read-only inspection of local Git stashes. Flag uncertain cases for manual review. No automatic `drop`, `clear`, `apply`, or branch operations.

## Research only: `denver`

Investigate whether public GitHub issue and commit metadata can reliably suggest otherwise unlinked fixes. Validate examples before committing to an implementation. A candidate match must never be presented as a verified fix without evidence.

## Not in the initial scope

Background daemons, servers, databases, automatic recovery claims, AI API integrations, and a general plugin framework.

The priority is one dependable tool, not a large command count.
