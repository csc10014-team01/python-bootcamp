"""Tests for the study planner help feature (shared.study_planner.help)."""

from shared.study_planner.help import SUPPORTED_FEATURES, Feature, help_text

# ---------------------------------------------------------------------------
# SUPPORTED_FEATURES contract
# ---------------------------------------------------------------------------


def test_supported_features_not_empty():
    """Registry must contain at least one entry."""
    assert len(SUPPORTED_FEATURES) >= 1


def test_supported_features_all_pairs():
    """Every entry must be a 2-tuple of non-empty strings."""
    for item in SUPPORTED_FEATURES:
        description, example = item
        assert isinstance(description, str) and description.strip()
        assert isinstance(example, str) and example.strip()


# ---------------------------------------------------------------------------
# help_text() output
# ---------------------------------------------------------------------------


def test_help_text_returns_str():
    assert isinstance(help_text(), str)


def test_help_text_not_empty():
    assert help_text().strip()


def test_help_text_contains_all_descriptions():
    """Every feature description must appear in the rendered output."""
    result = help_text()
    for description, _ in SUPPORTED_FEATURES:
        assert description in result, f"Missing description: {description!r}"


def test_help_text_contains_all_examples():
    """Every CLI example must appear in the rendered output."""
    result = help_text()
    for _, example in SUPPORTED_FEATURES:
        assert example in result, f"Missing example: {example!r}"


def test_help_text_custom_features():
    """help_text() must accept a custom feature list."""
    custom: list[Feature] = [
        ("Do something", "python -m shared.study_planner something"),
    ]
    result = help_text(custom)
    assert "Do something" in result
    assert "python -m shared.study_planner something" in result


def test_help_text_empty_features():
    """help_text() with an empty list must return the header only."""
    result = help_text([])
    assert "Study Planner" in result
    # No bullet points
    assert "•" not in result


# ---------------------------------------------------------------------------
# CLI integration — main() 'help' subcommand
# ---------------------------------------------------------------------------


def test_main_help_exits_zero(capsys):
    """main(['help']) must print help text and return 0."""
    from shared.study_planner.__main__ import main

    code = main(["help"])
    assert code == 0


def test_main_help_prints_output(capsys):
    """main(['help']) must produce non-empty stdout and nothing on stderr."""
    from shared.study_planner.__main__ import main

    main(["help"])
    captured = capsys.readouterr()
    assert captured.out.strip()
    assert captured.err == ""


def test_main_help_output_contains_feature(capsys):
    """At least one feature description must appear in the CLI output."""
    from shared.study_planner.__main__ import main

    main(["help"])
    captured = capsys.readouterr()
    description, _ = SUPPORTED_FEATURES[0]
    assert description in captured.out


def test_main_normal_still_works(capsys):
    """Existing CSV-based workflow must be unaffected by the help intercept."""
    import tempfile
    from pathlib import Path

    from shared.study_planner.__main__ import main

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "tasks.csv"
        csv_file.write_text(
            "title,importance,effort_h,deadline\n" "Test task,5,1,2030-01-01\n"
        )
        code = main([str(csv_file), "--hours", "2", "--today", "2026-10-26"])

    assert code == 0
    out = capsys.readouterr().out
    assert "Test task" in out


# ---------------------------------------------------------------------------
# Improvement 1 – case-insensitive 'help' recognition
# ---------------------------------------------------------------------------


def test_main_help_lowercase(capsys):
    """main(['help']) must be recognised (lowercase)."""
    from shared.study_planner.__main__ import main

    assert main(["help"]) == 0
    assert capsys.readouterr().out.strip()


def test_main_help_uppercase(capsys):
    """main(['HELP']) must be recognised (uppercase)."""
    from shared.study_planner.__main__ import main

    assert main(["HELP"]) == 0
    assert capsys.readouterr().out.strip()


def test_main_help_mixed_case(capsys):
    """main(['Help']) must be recognised (mixed case)."""
    from shared.study_planner.__main__ import main

    assert main(["Help"]) == 0
    assert capsys.readouterr().out.strip()


# ---------------------------------------------------------------------------
# Improvement 2 – reject unexpected extra arguments
# ---------------------------------------------------------------------------


def test_main_help_extra_arg_returns_2(capsys):
    """main(['help', 'abc']) must return exit code 2."""
    from shared.study_planner.__main__ import main

    code = main(["help", "abc"])
    assert code == 2


def test_main_help_extra_arg_writes_stderr(capsys):
    """main(['help', 'abc']) must write an error message to stderr."""
    from shared.study_planner.__main__ import main

    main(["help", "abc"])
    captured = capsys.readouterr()
    assert captured.err.strip()  # something on stderr
    assert captured.out == ""  # nothing on stdout


def test_main_help_extra_arg_no_stdout(capsys):
    """main(['help', 'abc']) must not print help text to stdout."""
    from shared.study_planner.__main__ import main

    main(["help", "abc"])
    assert capsys.readouterr().out == ""


# ---------------------------------------------------------------------------
# Improvement 3 – argparse --help still works (passthrough unaffected)
# ---------------------------------------------------------------------------


def test_main_argparse_help_is_passthrough():
    """--help must still be handled by argparse (raises SystemExit(0))."""
    import pytest

    from shared.study_planner.__main__ import main

    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0
