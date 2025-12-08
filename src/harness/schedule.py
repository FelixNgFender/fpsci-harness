import json
import logging
import pathlib
from typing import IO

import pydantic

from harness import types

logger = logging.getLogger(__name__)


class ParticipantSchedule(pydantic.BaseModel):
    participant: int
    games_with_latencies: list[types.GameWithLatencies]


class Schedule(pydantic.BaseModel):
    participants: list[ParticipantSchedule]

    def to_json(self, out: IO | pathlib.Path) -> None:
        """Write schedule to a JSON file or file-like object."""
        data = []
        for item in self.participants:
            entry = {
                "participant": item.participant,
                "games_with_latencies": [
                    {
                        "game": gwl.game.value,
                        "latencies": list(gwl.latencies),
                    }
                    for gwl in item.games_with_latencies
                ],
            }
            data.append(entry)

        if isinstance(out, pathlib.Path):
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open("w", encoding="utf8") as f:
                json.dump(data, f, indent=2)
        else:
            json.dump(data, out, indent=2)

    @classmethod
    def load_json(cls, path: pathlib.Path) -> "Schedule":
        with path.open("r", encoding="utf8") as f:
            raw = json.load(f)

        participants = []
        for entry in raw:
            participant = int(entry["participant"])

            games_with_latencies = [
                types.GameWithLatencies(
                    game=types.Game(g["game"]),
                    latencies=tuple(g["latencies"]),
                )
                for g in entry["games_with_latencies"]
            ]

            participants.append(
                ParticipantSchedule(
                    participant=participant,
                    games_with_latencies=games_with_latencies,
                )
            )

        return Schedule(participants=participants)


def _cyclic_latin_square(n: int) -> list[list[int]]:
    return [[(r + c) % n for c in range(n)] for r in range(n)]


def generate(games_with_latencies: list[types.GameWithLatencies]) -> Schedule:
    """
    Counterbalances:
      - game order (Latin square, size = number of games)
      - latency order (Latin square, size = 3)
    """

    games = games_with_latencies
    n_games = len(games)

    game_ls = _cyclic_latin_square(n_games)
    latency_ls = _cyclic_latin_square(3)  # LO/MED/HI

    participants = []
    pid = 0

    for game_row in game_ls:
        for lat_row in latency_ls:
            pid += 1

            reordered = []
            for g_idx in game_row:
                gwl = games[g_idx]

                # reorder latencies via LS
                new_latencies: tuple[int, int, int] = tuple(gwl.latencies[i] for i in lat_row)  # pyright: ignore[reportAssignmentType]

                reordered.append(
                    types.GameWithLatencies(
                        game=gwl.game,
                        latencies=new_latencies,
                    )
                )

            participants.append(
                ParticipantSchedule(
                    participant=pid,
                    games_with_latencies=reordered,
                )
            )

    return Schedule(participants=participants)
