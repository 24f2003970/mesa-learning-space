"""Shared umbrellas: two-phase activation, individual memory and a conserved pool.

AI assistance was used to prepare this teaching scaffold. It does not contain
the repository owner's personal motivation or claimed learning experiences.
"""

from __future__ import annotations

from mesa import Agent, Model
from mesa.datacollection import DataCollector


class Borrower(Agent):
    """A person who borrows at most one umbrella until their trip ends."""

    def __init__(self, model: UmbrellaLibrary) -> None:
        super().__init__(model)
        self.return_day: int | None = None
        self.loans = 0
        self.returns = 0
        self.missed = 0

    @property
    def has_umbrella(self) -> bool:
        return self.return_day is not None

    def return_if_due(self) -> None:
        if self.return_day is not None and self.return_day <= self.model.day:
            self.model.available += 1
            self.returns += 1
            self.return_day = None

    def try_borrow(self) -> None:
        if not self.model.raining or self.has_umbrella:
            return
        self.model.requests_today += 1
        if self.model.available > 0:
            self.model.available -= 1
            self.return_day = self.model.day + self.model.trip_days
            self.loans += 1
            self.model.served_today += 1
        else:
            self.missed += 1
            self.model.missed_today += 1


class UmbrellaLibrary(Model):
    """A station lends reusable umbrellas to a fixed group of borrowers.

    Each day: return all due umbrellas, draw shared weather, activate borrowers
    in shuffled order, then collect data. The pool has no losses or new supply.
    """

    def __init__(
        self,
        n_agents: int = 6,
        umbrellas: int = 2,
        trip_days: int = 2,
        rain_probability: float = 0.7,
        seed: int = 7,
    ) -> None:
        for name, value, minimum in [
            ("n_agents", n_agents, 1),
            ("umbrellas", umbrellas, 0),
            ("trip_days", trip_days, 1),
        ]:
            if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
                raise ValueError(f"{name} must be an integer >= {minimum}")
        if not 0 <= rain_probability <= 1:
            raise ValueError("rain_probability must be between 0 and 1")
        super().__init__(rng=seed)
        self.day = 0
        self.total_umbrellas = umbrellas
        self.available = umbrellas
        self.trip_days = trip_days
        self.rain_probability = rain_probability
        self.raining = False
        self.requests_today = 0
        self.served_today = 0
        self.missed_today = 0
        for _ in range(n_agents):
            Borrower(self)  # Mesa automatically registers each agent.
        self.datacollector = DataCollector(
            model_reporters={
                "day": "day",
                "rain": "raining",
                "available": "available",
                "held": lambda model: model.held,
                "requests": "requests_today",
                "served": "served_today",
                "missed": "missed_today",
            },
            agent_reporters={
                "has_umbrella": "has_umbrella",
                "loans": "loans",
                "returns": "returns",
                "missed": "missed",
            },
        )
        self.datacollector.collect(self)  # Day zero is the initial state.

    @property
    def held(self) -> int:
        return sum(agent.has_umbrella for agent in self.agents)

    def check_conservation(self) -> None:
        """Detect missing/duplicated umbrellas without relying on Python asserts."""
        if self.available < 0 or self.available + self.held != self.total_umbrellas:
            raise RuntimeError("Umbrella conservation was violated")

    def step(self) -> None:
        self.day += 1
        self.requests_today = self.served_today = self.missed_today = 0
        self.agents.do("return_if_due")
        # NumPy weather draws and stdlib activation shuffling use distinct streams.
        self.raining = bool(self.rng.random() < self.rain_probability)
        self.agents.shuffle_do("try_borrow")
        self.check_conservation()
        self.datacollector.collect(self)
