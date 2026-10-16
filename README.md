# Umbrella Library

A Mesa simulation of people borrowing umbrellas from a shared station. It explores how limited stock, trip length and rainy weather affect who gets an umbrella and how often requests go unserved.

## How It Works

Each borrower remembers whether they have an umbrella and when it is due back. One simulation step represents a day:

1. Borrowers return umbrellas whose trips have ended.
2. The model draws the day's weather.
3. On rainy days, people without umbrellas try to borrow in shuffled order.
4. The model records loans, returns, missed requests and remaining stock.

Borrowing immediately reduces the shared stock. A person already on a trip does not request another umbrella. Dry days still allow returns. Throughout the simulation, `available + held == total_umbrellas`.

The seed controls weather and activation order. Shuffling changes who gets served, but does not guarantee fairness in a short run. This is a small illustrative model, without spatial movement or calibrated weather data. See the [model walkthrough](models/umbrella_library/README.md) for details.

## Getting Started

Install Git and [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

```console
git clone https://github.com/24f2003970/mesa-learning-space.git
cd mesa-learning-space
uv sync --locked
uv run umbrella-demo --agents 3 --umbrellas 1 --trip-days 2 --days 4 --rain 1 --seed 7
```

Python 3.12 or newer is required; `.python-version` selects 3.14. Mesa is pinned to development commit `5451086fe47ab78e9ba894aa1b4c3063f4c247f1` (4.0.0a0), and `uv.lock` records the dependencies.

Change `--agents`, `--umbrellas`, `--trip-days`, `--rain` or `--seed` to compare scenarios. Optional CSV output uses a new filename and refuses to overwrite an existing file:

```console
uv run umbrella-demo --days 10 --seed 7 --csv run-7.csv
```

The output directory must already exist. `--rain` is a probability from 0 to 1; `--days 0` shows only the initial state.

## Example Output

The four-day command above produces:

```text
 day  rain  available  held  requests  served  missed
   0 False          1     0         0       0       0
   1  True          0     1         3       1       2
   2  True          0     1         2       0       2
   3  True          0     1         3       1       2
   4  True          0     1         2       0       2
Successful loans: 2
Returns: 1
Unserved requests: 8
Conservation: 0 available + 1 held = 1
```

The first umbrella returns on day 3 and can be borrowed again that day. A successful loan starts a trip; it is counted separately from a return. Day 0 records the initial state.

## Project Structure

- [model.py](models/umbrella_library/model.py): borrowers, daily activation and data collection.
- [run.py](models/umbrella_library/run.py): command-line options and CSV export.
- [tests/](tests/): model behavior, reproducibility and command-line checks.
- [notes/hands_on.md](notes/hands_on.md): exercises for exploring the model.

## Testing

```console
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

The suite has 51 tests covering return timing, conservation, scarcity, seeded histories, invalid inputs and CSV overwrite protection. Recorded Windows results and example comparisons are in [VALIDATION.md](VALIDATION.md).

Code, tests and documentation were prepared with AI assistance.

Licensed under the [MIT License](LICENSE). Repository structure originated from Mesa's [GSoC learning-space template](https://github.com/mesa/GSoC-learning-space); its original guide is retained in [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md).
