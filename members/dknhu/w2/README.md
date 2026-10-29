# dknhu — Week 2

- W2-1: `models.py` defines `Task`, validates importance, and clamps `days_left()` to zero.
- W2-2: `io_utils.py` loads CSV records and saves UTF-8 JSON with ISO dates. Invalid CSV headers and rows report their line number.
- W2-3: `errors.py` defines `InfeasiblePlan` and checks the total effort against the available hours.
- W2-4: `tests_for_MariiiMariii_tech.py` restores the peer tests from commit `bbd6087`, including cases absent from the instructor's tests: alphabetical frequency ties, `k=0`, and punctuation-only input.
- W2-5: `__init__.py` and `__main__.py` make the folder executable as a package.
- T-W2: `prioritise()` and its tests were already merged in PR #27; the shared contract was approved in PR #26.

Run from the repository root:

```bash
python -m members.dknhu.w2
python -m members.dknhu.w2 samples/tasks.csv
python -m pytest -q tests/test_w2.py tests/test_dknhu_w2.py tests/test_prioritise.py --member dknhu
python -m pytest -q members/dknhu/w2/tests_for_MariiiMariii_tech.py
python -m ruff check members/dknhu/w2 tests/test_dknhu_w2.py
```

Validation:

- Instructor W2 tests, additional W2 cases, and prioritise tests: **32 passed**.
- Default repository suite: **86 passed, 11 skipped** (the instructor's member-specific suites need `--member`).
- Peer suite: **25 passed, 1 failed**.
- Ruff: passed for the changed Python files and for the repository with the CI defaults.

The peer suite currently detects a W1 API mismatch: Mari's translation module defines `sieve_of_eratosthenes()` but the instructor requires `primes_up_to()`. The test intentionally reports that failure. W2-4 still needs the reviewee's response in this PR; the Week B rotation assignment should also be confirmed with the team. The default pytest discovery does not collect `tests_for_*.py`, so run the peer command explicitly.

AI assistance: Codex helped implement the missing W2 modules, restore the peer tests, and run validation.
