"""Behavioral checks for conservation, timing, scarcity and reproducibility."""

import pandas as pd
import pytest

from models.umbrella_library import UmbrellaLibrary


def test_two_day_trip_returns_before_borrowing() -> None:
    model = UmbrellaLibrary(n_agents=1, umbrellas=1, trip_days=2, rain_probability=1)
    agent = next(iter(model.agents))
    model.step()
    assert (model.day, model.time, model.available, agent.return_day, agent.loans) == (
        1,
        1,
        0,
        3,
        1,
    )
    model.step()
    assert (agent.return_day, agent.loans, model.requests_today) == (3, 1, 0)
    model.step()
    assert (agent.return_day, agent.loans, model.served_today) == (5, 2, 1)


def test_returns_are_not_counted_twice() -> None:
    model = UmbrellaLibrary(n_agents=1, umbrellas=1, trip_days=1, rain_probability=1)
    model.step()
    agent = next(iter(model.agents))
    model.day = 2
    agent.return_if_due()
    agent.return_if_due()
    assert model.available == 1 and not agent.has_umbrella
    assert agent.returns == 1
    model.check_conservation()


@pytest.mark.parametrize("seed", [0, 7, 42])
@pytest.mark.parametrize("rain", [0, 0.5, 1])
@pytest.mark.parametrize("umbrellas", [0, 2, 10])
def test_conservation_through_random_trajectories(seed, rain, umbrellas) -> None:
    model = UmbrellaLibrary(
        n_agents=6, umbrellas=umbrellas, rain_probability=rain, seed=seed
    )
    for _ in range(20):
        model.step()
        assert 0 <= model.available <= umbrellas
        assert model.available + model.held == umbrellas
        assert all(a.loans - a.returns == int(a.has_umbrella) for a in model.agents)
        assert model.requests_today == model.served_today + model.missed_today
    assert len(model.datacollector.get_model_vars_dataframe()) == 21
    assert len(model.datacollector.get_agent_vars_dataframe()) == 6 * 21


def test_no_umbrellas_means_all_rainy_requests_are_missed() -> None:
    model = UmbrellaLibrary(n_agents=4, umbrellas=0, rain_probability=1)
    model.run_for(3)
    assert sum(a.loans for a in model.agents) == 0
    assert sum(a.missed for a in model.agents) == 12
    assert model.held == 0


def test_no_rain_means_no_requests() -> None:
    model = UmbrellaLibrary(n_agents=4, umbrellas=2, rain_probability=0)
    model.run_for(5)
    assert model.available == 2
    assert sum(a.loans + a.missed for a in model.agents) == 0


def test_reference_four_day_example() -> None:
    model = UmbrellaLibrary(
        n_agents=3, umbrellas=1, trip_days=2, rain_probability=1, seed=7
    )
    model.run_for(4)
    table = model.datacollector.get_model_vars_dataframe()
    assert list(table["served"]) == [0, 1, 0, 1, 0]
    assert list(table["missed"]) == [0, 2, 2, 2, 2]
    assert sum(a.loans for a in model.agents) == 2
    assert sum(a.missed for a in model.agents) == 8


def test_same_seed_reproduces_individual_and_model_histories() -> None:
    first = UmbrellaLibrary(seed=91)
    second = UmbrellaLibrary(seed=91)
    first.run_for(12)
    second.run_for(12)
    pd.testing.assert_frame_equal(
        first.datacollector.get_model_vars_dataframe(),
        second.datacollector.get_model_vars_dataframe(),
    )
    pd.testing.assert_frame_equal(
        first.datacollector.get_agent_vars_dataframe(),
        second.datacollector.get_agent_vars_dataframe(),
    )


def test_population_change_does_not_change_seeded_weather() -> None:
    small = UmbrellaLibrary(n_agents=2, seed=13)
    large = UmbrellaLibrary(n_agents=9, seed=13)
    small.run_for(15)
    large.run_for(15)
    assert list(small.datacollector.get_model_vars_dataframe()["rain"]) == list(
        large.datacollector.get_model_vars_dataframe()["rain"]
    )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"n_agents": 0},
        {"n_agents": True},
        {"n_agents": 2.5},
        {"umbrellas": -1},
        {"umbrellas": False},
        {"trip_days": 0},
        {"trip_days": 1.2},
        {"rain_probability": -0.1},
        {"rain_probability": 1.1},
        {"rain_probability": float("nan")},
    ],
)
def test_invalid_parameters_are_rejected(kwargs) -> None:
    with pytest.raises(ValueError):
        UmbrellaLibrary(**kwargs)


def test_due_umbrellas_return_even_on_dry_days() -> None:
    model = UmbrellaLibrary(n_agents=1, umbrellas=1, trip_days=1, rain_probability=1)
    model.step()
    model.rain_probability = 0
    model.step()
    agent = next(iter(model.agents))
    assert model.available == 1 and model.held == 0
    assert model.requests_today == 0
    assert (agent.loans, agent.returns) == (1, 1)
