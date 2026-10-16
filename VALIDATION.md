# Validation

Checks run by the coding assistant on Windows, Python 3.14.4, pinned upstream Mesa `5451086fe47ab78e9ba894aa1b4c3063f4c247f1` (4.0.0a0), pytest 9.1.1 and Ruff 0.16.10 on 2026-10-17 IST.

- `uv sync --locked`: passed.
- `python -m pytest -q --basetemp <new-unused-campaign-directory>`: 51 passed in 1.34s. A dedicated temporary directory avoids an unrelated local default-temp permissions problem; tests require no private data or services.
- `ruff check .`: passed.
- `ruff format --check .`: 11 files already formatted.
- `git diff --check`: passed.
- Installed `umbrella-demo` entry point executed for all three scenarios below.

| Scenario (3 agents, 4 rainy days, seed 7) | Loans | Returns | Missed | Available + held |
|---|---:|---:|---:|---|
| 1 umbrella, 2-day trips | 2 | 1 | 8 | 0 + 1 = 1 |
| 3 umbrellas, 2-day trips | 6 | 3 | 0 | 0 + 3 = 3 |
| 1 umbrella, 1-day trips | 4 | 3 | 8 | 0 + 1 = 1 |

Coverage includes return timing and dry-day returns; no double returns; conservation and request accounting across 27 seeded trajectories; no stock/no rain; exact four-day aggregate behavior; identical seeded model and agent histories; weather independence from population size; invalid inputs; CSV output and overwrite protection; zero-day and invalid CLI arguments.

Validation covers Windows and Python 3.14.4; other platforms and Python versions have not been tested for this project. These local checks do not establish remote CI results or completion of the personal learning exercises.

## Documentation verification — 2026-10-17 IST

After the documentation cleanup, `uv sync --locked`, Ruff checks, formatting checks and the documented reference simulation passed. The README output matches the captured CLI output exactly. CSV export and the walkthrough's individual-history example also ran successfully. Relative README links resolve to existing files; the uv installation page and both GitHub repository links were checked.

The full suite passed again: 51 tests in 1.29s with a fresh temporary directory. Running `uv run pytest -q` without that override produced 49 passes and two CSV-fixture setup errors because this workstation's default pytest temporary folder is inaccessible. For that environment issue, use `uv run pytest --basetemp <new-unused-directory>`; pytest manages and may remove the selected directory, so do not point it at existing work. No model, tests or dependency pins changed.
