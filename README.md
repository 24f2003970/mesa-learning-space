# Umbrella Library — Mesa learning space

A small agent-based model: people share a limited stock of reusable umbrellas. It demonstrates agent memory, phased scheduling, indirect interaction, reproducible randomness and data collection.

**AI assistance:** code, tests and technical documentation were prepared with AI assistance as a learning scaffold. This repository does not claim that the owner has already run or understood it. Personal motivation and reflections are intentionally left for the owner after hands-on work. No AI-generated personal GSoC statements are supplied.

Prerequisites: Git, Python and the `uv` package manager. Run the commands below from this repository directory. The first sync downloads dependencies.

## Run the first exercise

Python 3.12 or newer is required; `.python-version` selects 3.14. The Mesa development source is pinned to upstream commit `5451086`, independently of the campaign's local Mesa fix.

```console
uv sync --locked
uv run umbrella-demo --agents 3 --umbrellas 1 --trip-days 2 --days 4 --rain 1 --seed 7
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Expected summary: **2 successful loans, 1 return, 8 unserved requests; 0 available + 1 held = 1 umbrella**. A successful loan starts a trip; it is not counted as a completed trip. The detailed table includes the initial day-zero state.

Read the [model walkthrough](models/umbrella_library/README.md) before changing parameters. Then try 3 umbrellas and predict the result before running it.

- [Model code](models/umbrella_library/model.py) and [CLI](models/umbrella_library/run.py).
- [Executed validation and limitations](VALIDATION.md).
- [Behavior tests](tests/test_model.py), [CLI checks](tests/test_cli.py).
- [Hands-on worksheet](notes/hands_on.md): the owner's answers must come from actually running and understanding the model.
- [Original template guide](TEMPLATE_GUIDE.md) and untouched [personal motivation prompts](motivation.md).

This is an illustrative toy model, not a calibrated transport or weather prediction. No data, browser, credentials or server is needed. No Mesa PR or application is submitted from this repository; required personal sections and human peer review remain separate.
