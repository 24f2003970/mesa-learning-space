# Executed validation

Executed by the AI coding assistant on Windows, Python 3.14.4, pinned upstream Mesa `5451086fe47ab78e9ba894aa1b4c3063f4c247f1` (4.0.0a0), pytest 9.1.1 and Ruff 0.16.10 on 2026-10-17 IST.

- `uv sync --locked`: passed after enabling Hatch direct-reference metadata for the pinned Git dependency.
- `python -m pytest -q --basetemp <new-unused-campaign-directory>`: **51 passed in 1.34s**. A dedicated temporary directory avoids an unrelated local default-temp permissions problem; tests require no private data or services.
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

These are assistant-executed checks, not evidence that the repository owner has completed the learning exercises. Other operating systems and Python versions have not been tested for this learning project. No remote CI, calibrated realism, long-term fairness, Mesa maintainer acceptance, or completed personal GSoC requirements are claimed. The separate Mesa bug contribution's 872-test validation is not part of this project's 51-test result.
