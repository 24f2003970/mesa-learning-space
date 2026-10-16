"""Run the learning model from a terminal; no server or credentials required."""

import argparse
from pathlib import Path

from .model import UmbrellaLibrary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", type=int, default=6)
    parser.add_argument("--umbrellas", type=int, default=2)
    parser.add_argument("--trip-days", type=int, default=2)
    parser.add_argument("--days", type=int, default=8)
    parser.add_argument(
        "--rain", type=float, default=0.7, help="Daily rain probability, 0..1"
    )
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument(
        "--csv",
        type=Path,
        help="Optional new CSV file; existing files are not overwritten",
    )
    args = parser.parse_args(argv)
    if args.days < 0:
        parser.error("days must be nonnegative")
    if args.csv is not None and args.csv.exists():
        parser.error("CSV destination already exists; choose a new filename")
    try:
        model = UmbrellaLibrary(
            n_agents=args.agents,
            umbrellas=args.umbrellas,
            trip_days=args.trip_days,
            rain_probability=args.rain,
            seed=args.seed,
        )
    except ValueError as error:
        parser.error(str(error))
    if args.days:
        model.run_for(args.days)
    table = model.datacollector.get_model_vars_dataframe()
    print(table.to_string(index=False))
    print(f"Successful loans: {sum(a.loans for a in model.agents)}")
    print(f"Returns: {sum(a.returns for a in model.agents)}")
    print(f"Unserved requests: {sum(a.missed for a in model.agents)}")
    print(
        f"Conservation: {model.available} available + {model.held} held = {model.total_umbrellas}"
    )
    if args.csv is not None:
        # Exclusive creation closes the race between the earlier check and writing.
        with args.csv.open("x", encoding="utf-8", newline="") as stream:
            table.to_csv(stream, index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
