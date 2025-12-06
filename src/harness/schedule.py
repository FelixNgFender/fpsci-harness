import csv
import json
import logging
import pathlib
from typing import IO

import pydantic

from harness import settings

logger = logging.getLogger(__name__)


class ParticipantSchedule(pydantic.BaseModel):
    participant: int
    games: list[settings.Game]
    latencies: list[int]


class Schedule(pydantic.BaseModel):
    participants: list[ParticipantSchedule]

    def to_csv(self, out: IO) -> None:
        writer = csv.writer(out)
        writer.writerow(["participant", "games", "rounds"])

        for item in self.participants:
            writer.writerow(
                [
                    item.participant,
                    json.dumps([g.value for g in item.games]),
                    json.dumps(list(item.latencies)),
                ]
            )

    @classmethod
    def load_csv(cls, path: pathlib.Path) -> "Schedule":
        rows = []
        with path.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                participant = int(row["participant"])
                games = [settings.Game(g) for g in json.loads(row["games"])]
                latencies = [int(la) for la in json.loads(row["latencies"])]
                rows.append(ParticipantSchedule(participant=participant, games=games, latencies=latencies))
        return Schedule(participants=rows)


def _cyclic_latin_square(n: int) -> list[list[int]]:
    """Return Latin square as list of rows; each row is a list of symbols 0..n-1."""
    return [[(r + c) % n for c in range(n)] for r in range(n)]


def generate(experiment_settings: settings.ExperimentSettings) -> Schedule:
    """Generate an in-memory schedule."""

    ls_games = _cyclic_latin_square(len(experiment_settings.games))
    ls_latency = _cyclic_latin_square(len(experiment_settings.latencies))

    participants: list[ParticipantSchedule] = []
    for gi, game_row in enumerate(ls_games):
        for li, latency_row in enumerate(ls_latency):
            pid = gi * len(ls_latency) + li + 1
            game_order = [experiment_settings.games[i] for i in game_row]
            latency_order = [experiment_settings.latencies[i] for i in latency_row]

            participants.append(ParticipantSchedule(participant=pid, games=game_order, latencies=latency_order))

    return Schedule(participants=participants)
