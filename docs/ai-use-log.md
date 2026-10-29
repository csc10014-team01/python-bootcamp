# AI Use Log

This file records every interaction with AI tools during the `python-bootcamp` coursework.

---

## Entry 001

| Field | Value |
|-------|-------|
| **Date** | 2026-10-29 |
| **Task** | Lab 03 H1 – Help command for `shared.study_planner` |
| **Tool** | Antigravity (Google DeepMind) |
| **Branch** | `feat/lab03-help-review` |
| **Prompt summary** | Asked the AI to extend `shared.study_planner` with a `help` subcommand that prints supported features, following the existing module architecture, with unit tests and H1 documentation. |

### What the AI produced

- `shared/study_planner/help.py` — new module with `SUPPORTED_FEATURES` registry and `help_text()` formatter.
- `shared/study_planner/__main__.py` — pre-argparse intercept for `argv[0] == "help"`.
- `tests/test_help.py` — 12 pytest tests covering the registry contract, formatter output, and CLI integration.
- `docs/lab3/ai_extension_review.md` — H1 review document.
- `docs/ai-use-log.md` — this file.

### What I verified

*(Fill in after you run the tests and check the output yourself.)*

- [ ] `python -m shared.study_planner help` prints the feature list.
- [ ] `python -m shared.study_planner samples/tasks.csv --hours 2 --today 2026-10-26` still works.
- [ ] `pytest tests/test_help.py -v` — all 12 tests pass.
- [ ] `ruff check` — no errors.

### Changes I made after AI generation

**Feature:** Study Planner Help Command  
**AI Tool:** ChatGPT / AI Coding Assistant  
**Repository:** `python-bootcamp`

### Purpose of AI Use

AI was used to generate the initial implementation of the Help Command and assist with subsequent code revisions.

### Human Contribution

I reviewed the AI-generated code and identified three areas requiring improvement:

1. Case-sensitive Help Command recognition.
2. Missing validation for unexpected arguments.
3. Duplicated command-line argument handling.

I formulated specific correction requirements and instructed the AI to implement them.

### AI Contribution

The AI assisted with implementing the Help Command, revising the identified issues, and updating the relevant tests.

### Verification

I inspected the changes using Git diff and executed the automated test suite.

The initial pytest run encountered a Windows temporary-directory permission error. After using an alternative temporary directory, all tests passed.

### Disclosure

The source-code modifications were AI-assisted. My contribution focused on identifying issues, defining corrections, reviewing the implementation, and validating the results.

---

## Entry 002 — dknhu Week 2 (retrospective disclosure)

- Date: 2026-10-29.
- Tool: OpenAI Codex.
- Branch: `feat/w2-dknhu-complete`.
- PR: [#45](https://github.com/csc10014-team01/python-bootcamp/pull/45), merged.
- Prompt summary: dknhu asked Codex to audit the Week 2 requirements and then complete the missing work.
- Generated code retained: `members/dknhu/w2/{__init__,__main__,models,io_utils,errors}.py`, the additional tests in `tests/test_dknhu_w2.py`, and W2 documentation. Codex restored the peer suite from commit `bbd6087` and prepared the PR/progress entry.
- Verification performed by Codex: 32 W2/prioritise tests passed; the default repository suite had 86 passed and 11 skipped; Ruff and GitHub CI passed. The explicit peer suite had 25 passed and 1 failed because Mari's W1 module lacks `primes_up_to()`.
- The PR already disclosed AI assistance. This entry adds the disclosure to the required repository log. Human review and the reviewee's response were not performed by Codex and are not claimed here.

## Entry 003 — dknhu Week 3

- Date: 2026-10-29.
- Tool: OpenAI Codex.
- Branch: `py/w3-dknhu`.
- Prompt summary: dknhu asked Codex to continue their work against the supplied Week 3, progress-tracking, review, and AI-disclosure requirements.
- Generated code retained: the date parser, route statistics, study CLI, tests, and README under `members/dknhu/w3/`; a dedicated `.github/workflows/dknhu.yml` running the instructor's tests with the correct member/variant; type hints, docstrings, and formatting changes in dknhu's earlier code and tests.
- Other generated material retained: this log entry, the retrospective W2 disclosure, the W3 progress entry, and the W3 PR description including the three-line Python/C++ comparison.
- Verification performed by Codex: the instructor's W1/W2/W3 tests and targeted regression suite passed (89 tests); the complete repository with dknhu's member/variant selected passed all 142 tests. Default discovery had 131 passed and 11 skipped. Ruff and formatting checks passed. An AST check found complete parameter/return annotations and docstrings in all 71 authored functions checked. The W3 suite tests date boundaries, p95 rank selection, empty input, malformed data, the current-date default, and real CLI execution. These totals exclude the separately invoked W2 peer suite and its known failure described above.
- Human contribution recorded: dknhu supplied the requirements and requested implementation. Personal review, individual-defence preparation, actual study hours, and assigned teammate review still require dknhu's participation; this entry does not claim those have happened.
- Commit dates use the actual work date; no historical activity or human-only authorship is fabricated.
