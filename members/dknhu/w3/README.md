# dknhu — Week 3

## Deliverables

- W3-1: `dates.parse_due(text, today)` handles ISO dates, tomorrow, non-negative relative days, and the next English weekday. A matching weekday means seven days later.
- W3-2: `log_stats.analyse(pairs)` returns a `Counter` of requests, per-route nearest-rank p95 latencies, and the route with the highest p95. Empty input has `slowest=None`; ties keep the first route encountered.
- W3-3: `cli.py` reuses the W2 task loader and `Task.days_left()`. It sorts by `importance / max(days_left, 1)` and greedily assigns hours, including a partial final task.
- W3-4: dknhu's W1–W3 functions and tests have parameter/return annotations and docstrings. Earlier personal contributions to the shared prioritiser and end-to-end tests are documented too.
- T-W3: the sample-CSV pipeline and CLI end-to-end tests were already merged in [PR #40](https://github.com/csc10014-team01/python-bootcamp/pull/40).

## Run

```bash
python -m members.dknhu.w3.cli samples/tasks.csv --hours 2 --today 2026-10-26
```

```text
Tonight (2.0 h):
  1. Assignment ........ 1.5 h
  2. DS exam ........... 0.5 h
```

Omitting `--today` uses `date.today()`. File/data errors print to stderr and exit with status 1; invalid arguments use argparse's status 2. A valid CSV header with no rows prints an empty plan. Zero hours is valid; negative or non-finite hours are rejected.

```bash
python -m pytest -q members/dknhu/w3 tests/test_w3.py --member dknhu
python -m pytest -q tests/test_w1.py tests/test_w2.py tests/test_w3.py tests/test_dknhu_w2.py tests/test_prioritise.py tests/test_study_planner_e2e.py members/dknhu/w3 --member dknhu --variant 3
python -m ruff check members/dknhu
```

The dedicated `dknhu homework` workflow supplies `--member dknhu --variant 3` so the instructor's tests actually run in CI. The generic repository workflow skips those tests when no member is selected.

Validation performed by Codex:

- W3 tests including the instructor's suite: **48 passed**.
- W1–W3 instructor tests plus personal/team regression tests: **89 passed**.
- Full repository with `--member dknhu --variant 3`: **142 passed, no skips**.
- Default repository discovery: **131 passed, 11 skipped**.
- Ruff checks and formatting checks passed; all 71 inspected authored functions have parameter/return annotations and docstrings.

These totals exclude the explicitly invoked W2 peer suite, whose known missing-API failure is documented in PR #45 and the AI use log.

## Concepts to explain during the individual defence

- `timedelta` performs calendar arithmetic; modulo seven finds a weekday offset, and `or 7` prevents selecting today for a weekday expression.
- `Counter` counts routes, while `defaultdict(list)` groups their observed latencies. Nearest-rank p95 selects index `ceil(0.95 * n) - 1` from a sorted copy. With twenty samples, that is the nineteenth sample, not necessarily the maximum.
- `sorted()` creates a new list. The planner stores assigned hours separately from each task, so partial allocation never changes the task's original effort.
- Type hints document expectations and help tools; they do not enforce argument types at runtime. Runtime checks still reject invalid dates, budgets, and CSV records.
- File errors return 1 from `main()`, and `SystemExit(main())` forwards that result to the shell. Argument errors are handled by argparse.

Python/C++ reflection (three lines, also included in the PR):

1. Python feature highlighted: list comprehensions, as used in the W1 matrix transpose.
2. A nested comprehension builds output rows directly from input columns.
3. Compared with explicit C++ loops and `push_back`, the expression states the result to construct.

## Progress and review evidence

W2 individual work was merged in [PR #45](https://github.com/csc10014-team01/python-bootcamp/pull/45), and T-W3 work in PR #40. W3 still needs the assigned reviewer's approval and merging; the Week C reviewer and actual hours have not been supplied. Review comments should include a concrete Question, Suggestion, and Praise after reading the assigned teammate's code.

The commits made in this session share the real work date. They do not claim work spread over several days. Team completion tags should only be created after all team deliverables meet the course criteria.

AI-generated code retained in this work is disclosed in `docs/ai-use-log.md` and the PR. The automated checks were run by Codex; dknhu still needs to review and be able to explain the code personally.
