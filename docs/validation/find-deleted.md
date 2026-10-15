# `find-deleted`: real-world validation baseline

> **Historical review record — 2026-10-15.** This document transcribes the independent agent's completed validation report supplied for [Git Phew PR #2](https://github.com/ahmet-izgi/git-phew/pull/2) at **exact head** [`4368c12fede66470b0f0c2c90914f0fb233b2fea`](https://github.com/ahmet-izgi/git-phew/commit/4368c12fede66470b0f0c2c90914f0fb233b2fea). It is **not** a claim that later PR revisions passed these tests. These results were reported by the reviewer and archived here; this documentation-only change **does not independently rerun the experiments**.

**Review decision at this head: CHANGES REQUIRED.** Twenty independently selected real removals were matched, but two additional reproductions exposed a terminal-output safety flaw and a valid-Python false negative. Neither problem should be erased from the record when fixed.

## Scope and method

The reviewer reported that each of the 20 removal events was chosen **independently of Git Phew's search results**, from distinct commits. Ground truth was established using native Git parent/child blobs and AST comparison **before** invoking Git Phew. The identified function occurred once in the prior file and was absent from the corresponding file after the change. The reviewer then checked the recovered path, source text and removal commit against that ground truth.

The result is **per-file removal evidence**, not evidence that a function is absent throughout the project. Correctly reporting a function's removal from an old file when it moves elsewhere is within the reviewed semantics.

### Pinned upstream repository heads

| Upstream repository | Pinned HEAD |
| --- | --- |
| [psf/requests](https://github.com/psf/requests) | [`611c6162cbc4ac2020a2f91c7cfa4f3abf9bbb60`](https://github.com/psf/requests/commit/611c6162cbc4ac2020a2f91c7cfa4f3abf9bbb60) |
| [pallets/flask](https://github.com/pallets/flask) | [`d086db856be187255b8ec61ef409357393020f32`](https://github.com/pallets/flask/commit/d086db856be187255b8ec61ef409357393020f32) |
| [encode/httpx](https://github.com/encode/httpx) | [`b5addb64f0161ff6bfe94c124ef76f6a1fba5254`](https://github.com/encode/httpx/commit/b5addb64f0161ff6bfe94c124ef76f6a1fba5254) |

## 20 verified removal events

For every row, the **independently established expected result** was a single removal of the named function from the listed file at that commit, with recoverable prior source. **Actual** was the expected path, exact source and commit with exit code 0, as reported by the reviewer. File deletions refer to the whole Python file being removed. The linked SHA is the removal commit, **not** the repository's pinned HEAD.

| # | Repository | Function | Removal commit | Expected previous path | Scenario | Actual | Result |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | requests | `ssl_wrap_socket` | [`99fa7becf263`](https://github.com/psf/requests/commit/99fa7becf263473c7bfc1998b41c2c6c80a0f499) | `requests/packages/urllib3/contrib/pyopenssl.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 2 | requests | `__str__` | [`c15a8f8a3d8f`](https://github.com/psf/requests/commit/c15a8f8a3d8fbe943dcae2603c4ceca7f99ff2bf) | `requests/structures.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 3 | requests | `detect` | [`480a3821ab9e`](https://github.com/psf/requests/commit/480a3821ab9ebfdd0830ad9907b99af99d251e66) | `requests/packages/chardet/__init__.py` | File deletion | Exact path, source and removal commit; exit 0 | PASS |
| 4 | requests | `header_expand` | [`c3431bb6f21b`](https://github.com/psf/requests/commit/c3431bb6f21bf7c88ff86d9a232ba4db54bb91a0) | `requests/utils.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 5 | requests | `iter_json` | [`def20cdb0cf1`](https://github.com/psf/requests/commit/def20cdb0cf1d4fcc3aa4cd3164602d6c4029ac3) | `requests/models.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 6 | requests | `_build_response` | [`4a01272fb3a5`](https://github.com/psf/requests/commit/4a01272fb3a56d718c82305e40d967dc0318bd32) | `requests/models.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 7 | requests | `full_url` | [`ab27027aa891`](https://github.com/psf/requests/commit/ab27027aa8916e6e199bbb35083beb5d6339f6aa) | `requests/models.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 8 | flask | `_json_loads` | [`41aaaf7fa07f`](https://github.com/pallets/flask/commit/41aaaf7fa07f28ef15fd1d343142e96440889a8b) | `src/flask/config.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 9 | flask | `_reconfigure_for_run_debug` | [`2433522d2967`](https://github.com/pallets/flask/commit/2433522d2967b8a5e46f16de587a8fac5088a47c) | `flask/app.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 10 | flask | `should_log_for` | [`7c16054d81ce`](https://github.com/pallets/flask/commit/7c16054d81ce9af44a4875650b506c9ec2403588) | `flask/logging.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 11 | flask | `register_module` | [`817b72d484d3`](https://github.com/pallets/flask/commit/817b72d484d353800d907b3580c899314bf7f3c6) | `flask/app.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 12 | flask | `without_appcontext` | [`932f7d7cbb5a`](https://github.com/pallets/flask/commit/932f7d7cbb5a4e04fd0922c3272a6e32d408abe8) | `flask/cli.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 13 | flask | `get_body` | [`4c27f7a8c4bb`](https://github.com/pallets/flask/commit/4c27f7a8c4bbe6621681178be716e6270067a3ad) | `flask/exceptions.py` | File deletion | Exact path, source and removal commit; exit 0 | PASS |
| 14 | flask | `_tojson_filter` | [`b146d8277ab9`](https://github.com/pallets/flask/commit/b146d8277ab90cf6d43ea54113383076e4fd0318) | `flask/helpers.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 15 | httpx | `port_or_default` | [`7b19cd5f4b74`](https://github.com/encode/httpx/commit/7b19cd5f4b749064c6452892a5e58a3758da1d1b) | `httpx/_utils.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 16 | httpx | `is_known_encoding` | [`41597adffa9d`](https://github.com/encode/httpx/commit/41597adffa9d34171a63f7511fc0f702558dd08c) | `httpx/_utils.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 17 | httpx | `format_form_param` | [`6212e8fa3bf9`](https://github.com/encode/httpx/commit/6212e8fa3bf90154b891c7721f6d29737caac861) | `httpx/_utils.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 18 | httpx | `normalize_header_key` | [`83a85189c797`](https://github.com/encode/httpx/commit/83a85189c79708b732d04e7b906e388fb0fbde94) | `httpx/_utils.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 19 | httpx | `load_ssl_context` | [`8e36f2bc685d`](https://github.com/encode/httpx/commit/8e36f2bc685dfbe43cd7503bc1c422a6ed6e05a5) | `httpx/_config.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |
| 20 | httpx | `guess_json_utf` | [`1d73150c1f66`](https://github.com/encode/httpx/commit/1d73150c1f663757d63585aecfcb329d0ec00825) | `httpx/_utils.py` | Function removal | Exact path, source and removal commit; exit 0 | PASS |

**Observed outcome within this positively selected sample: 20/20 correct.** This is not a measured 100% recall rate over all possible removals or Python syntax.

## Additional real-history scenarios

- **Signature edit (expected no removal):** HTTPX `httpx/_api.py` retained `request` across commit [`80960fa31918d7663c3f4c3ad61661cf0e80628f`](https://github.com/encode/httpx/commit/80960fa31918d7663c3f4c3ad61661cf0e80628f). Git Phew returned **exit 1** as expected.
- **File rename retaining a function:** Requests renamed `test_requests.py` to `tests/test_requests.py` in [`18b26d20f7d0623e4b3df9fa6538e86069df3cdb`](https://github.com/psf/requests/commit/18b26d20f7d0623e4b3df9fa6538e86069df3cdb). `test_get` remained present; Git Phew returned **exit 1**.
- **Cross-file move (per-file semantics):** At that same Requests commit, `httpbin` moved from `test_requests.py` to `tests/conftest.py`. A removal from the old file was reported, **correct under the documented per-file meaning**; this does not imply project-wide deletion.
- **Multiple historical removals:** An unfiltered Requests query for `_build_response` produced **three candidates** and returned **exit 3**, refusing to select one automatically.
- **Not found independently in this real-history sample:** a same-file duplicate-definition event and a merge-only removal event. Synthetic tests or code reasoning do not replace missing real-history evidence.

These extra scenarios are **not included** in the 20-row positive-removal count.

## Aggregate results (reported)

| Measure | Result |
| --- | --- |
| Independently selected real-world removal events | 20 |
| Correct matches among those 20 | **20 / 20** |
| Misses among those 20 | 0 |
| False positive per-file removal claims in those 20 | 0 |
| **Additional** independently reproduced valid-syntax miss | **1 (see finding 2)** |
| Unexpected uncaught crashes observed | 0 |
| Unexpected repository changes observed | 0; three clone worktrees clean before and after |
| Local tests | 14/14 passed using Python 3.14 |
| GitHub CI at the exact baseline head | [Run 38664740714](https://github.com/ahmet-izgi/git-phew/actions/runs/38664740714): 4/4 passed |

The reviewer reported that `git phew -h` worked using a temporary Git command shim. A temporary package install was **not** completed because that Python 3.14 environment lacked `setuptools.build_meta`; no global installation was attempted. Python 3.14 also emitted non-fatal `SyntaxWarning` messages on some old source blobs with invalid escape sequences. Do not present that local installation attempt as a pass.

### Performance sample

Each query was executed **five times**. Times are reviewer-reported medians for that machine, not general performance guarantees.

| Repository (reported size) | Query | Candidate removals | Median runtime |
| --- | --- | ---: | ---: |
| HTTPX (1,523 commits; 12 MB clone) | `port_or_default` | 1 | 0.807 s |
| HTTPX (1,523 commits; 12 MB clone) | `git_phew_query_with_no_such_function_94721` | 0 | 0.283 s |
| Requests (6,495 commits; 19 MB clone) | `_build_response` | 3 | 0.935 s |

Flask was reported as 5,562 commits and a 15 MB clone; no Flask timing was supplied.

## Confirmed findings at baseline head

### MAJOR: terminal control sequences in untrusted repository output

**Location:** [`src/git_phew/cli.py`, approximately lines 63–80](https://github.com/ahmet-izgi/git-phew/blob/4368c12fede66470b0f0c2c90914f0fb233b2fea/src/git_phew/cli.py#L63-L80).

**Reproduction:** In a disposable Git repository, the reviewer deleted a Python file whose name contained the control sequence `ESC[2J`. A successful search printed the sequence as raw bytes in the terminal output. On many terminals, this clears displayed content. Other embedded path controls may visually forge or alter the output.

**Recommended minimum correction:** safely render all untrusted displayed paths, recovered source text and Git diagnostics, without unnecessarily destroying ordinary Unicode. Add exact-byte regression tests for control characters. Treat the confirmed filename reproduction separately from the broader audit of all display surfaces.

### MINOR: a valid continued function definition is missed

**Location:** [`src/git_phew/commands/find_deleted.py`, approximately lines 107–114](https://github.com/ahmet-izgi/git-phew/blob/4368c12fede66470b0f0c2c90914f0fb233b2fea/src/git_phew/commands/find_deleted.py#L107-L114).

**Reproduction:** Python accepts an explicit backslash continuation between `def` and the name:

```python
def \
    lost():
    return 1
```

The reviewer committed this function, removed it in a subsequent commit and independently confirmed the removal by Git and AST. Git Phew returned **exit 1** (no match). Its `git log -G` prefilter expects `def`, name and `(` on one line.

**Recommended minimum correction:** broaden or supplement the prefilter enough to include valid continued declarations while retaining the efficient Git-based preselection. Add a regression test; measure the impact on representative histories.

## Decision and follow-up

**CHANGES REQUIRED** at PR #2 head `4368c12fede66470b0f0c2c90914f0fb233b2fea`.

1. Fix terminal rendering and the continued-declaration false negative; add regression tests.
2. Re-run CI and focused correctness/security tests at the **new exact PR HEAD**.
3. Have the independent reviewer inspect the updated diff and verify the two reproductions.
4. Keep PR #2 unmerged and unreleased until the new head meets the acceptance criteria.

**Record integrity:** This page is an immutable *validation baseline in meaning*; a subsequent successful review should be recorded in an additional dated section or a separate follow-up document rather than silently replacing failure findings. This document records externally reported test evidence, not verification newly performed as part of its own documentation PR.
