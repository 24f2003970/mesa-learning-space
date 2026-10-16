"""The user-facing runner reports results and protects existing output files."""

import pandas as pd
import pytest

from models.umbrella_library.run import main


def test_cli_reference_example_and_csv(tmp_path, capsys) -> None:
    output = tmp_path / "trace.csv"
    assert (
        main(
            [
                "--agents",
                "3",
                "--umbrellas",
                "1",
                "--trip-days",
                "2",
                "--days",
                "4",
                "--rain",
                "1",
                "--seed",
                "7",
                "--csv",
                str(output),
            ]
        )
        == 0
    )
    trace = pd.read_csv(output)
    assert list(trace["served"]) == [0, 1, 0, 1, 0]
    text = capsys.readouterr().out
    assert "Successful loans: 2" in text and "Unserved requests: 8" in text
    assert "Conservation: 0 available + 1 held = 1" in text


def test_existing_csv_is_preserved(tmp_path) -> None:
    output = tmp_path / "existing.csv"
    output.write_text("keep this", encoding="utf-8")
    with pytest.raises(SystemExit) as error:
        main(["--csv", str(output)])
    assert error.value.code == 2
    assert output.read_text(encoding="utf-8") == "keep this"


def test_zero_days_reports_only_initial_state(capsys) -> None:
    assert main(["--days", "0"]) == 0
    assert "Successful loans: 0" in capsys.readouterr().out


@pytest.mark.parametrize("args", [["--days", "-1"], ["--agents", "0"], ["--rain", "2"]])
def test_invalid_cli_arguments(args) -> None:
    with pytest.raises(SystemExit) as error:
        main(args)
    assert error.value.code == 2
