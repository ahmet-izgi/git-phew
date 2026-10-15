# Roadmap (proposals, not commitments)

Git Phew will grow only when a narrowly scoped utility demonstrates a real benefit. No stable utility release has been published.

## First: `find-deleted` — experimental

Initial support is intentionally **Python functions only**. The command scans local commits reachable from HEAD and attempts to prove a function was removed from a specific file, showing its historical source and commit references. It never changes the working tree or refs.

Correctness tests must cover removals, signature edits that retain a function, renames, duplicate names, syntax errors, and dirty worktrees. Unsupported cases must fail conservatively. **Before release**, validate it on several real public Git histories, not just synthetic test repositories.

## Later candidate: `stash-audit`

Read-only inspection of local Git stashes. Flag uncertain cases for manual review. No automatic `drop`, `clear`, `apply`, or branch operations.

## Research only: `denver`

Investigate whether public GitHub issue and commit metadata can reliably suggest otherwise unlinked fixes. Validate examples before committing to an implementation. A candidate match must never be presented as a verified fix without evidence.

## Not in the initial scope

Background daemons, servers, databases, automatic recovery claims, AI API integrations, and a general plugin framework.

The priority is one dependable tool, not a large command count.
