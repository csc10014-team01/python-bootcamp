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
