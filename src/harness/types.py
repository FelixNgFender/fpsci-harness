import enum
from typing import NamedTuple


class Game(enum.StrEnum):
    """Add more games here."""

    FITTS = "fitts_law"
    FEEDING_FRENZY = "feeding_frenzy"
    ROCKET_LEAGUE = "rocket_league"
    DAVE_THE_DIVER = "dave_the_diver"
    HALF_LIFE_2 = "half_life_2"


class MonitoringChoice(enum.StrEnum):
    ALL = "all"
    KEYBOARD = "keyboard"
    MOUSE = "mouse"


class GameWithLatencies(NamedTuple):
    game: Game
    duration: int
    latencies: tuple[int, int, int, int]
