import csv
import logging
import pathlib

from harness import settings

logger = logging.getLogger(__name__)


def _cyclic_latin_square(n: int) -> list[list[int]]:
    """Return Latin square as list of rows; each row is a list of symbols 0..n-1."""
    return [[(r + c) % n for c in range(n)] for r in range(n)]


def generate(schedule_settings: settings.ScheduleSettings) -> None:
    """Generate a schedule CSV file containing experiment configurations based on latin squares"""

    # Build Latin squares
    ls_games = _cyclic_latin_square(len(schedule_settings.games))
    ls_latency = _cyclic_latin_square(len(schedule_settings.latencies))

    # Create participant schedules
    schedules = []
    for gi, game_row in enumerate(ls_games):
        for li, latency_row in enumerate(ls_latency):
            participant_id = gi * len(ls_latency) + li + 1  # participant 1..15

            game_order = [schedule_settings.games[i] for i in game_row]
            latency_order = [schedule_settings.latencies[i] for i in latency_row]

            per_game_rounds = {game: ["trial"] + [f"{ms}" for ms in latency_order] for game in game_order}

            schedules.append(
                {
                    "participant": participant_id,
                    "game_order": game_order,
                    "latency_order": latency_order,
                    "per_game_rounds": per_game_rounds,
                }
            )

    # Export to CSV
    csv_path = "latin_schedules.csv"

    with pathlib.Path(csv_path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # CSV header
        writer.writerow(
            [
                "participant",
                "game_position",
                "game_name",
                "round_1",
                "round_2",
                "round_3",
                "round_4",
            ]
        )

        # One row per (participant, game)
        for s in schedules:
            p = s["participant"]
            for pos, game in enumerate(s["game_order"], start=1):
                rounds = s["per_game_rounds"][game]
                writer.writerow(
                    [
                        p,
                        pos,
                        game,
                        rounds[0],  # trial
                        rounds[1],  # latency A
                        rounds[2],  # latency B
                        rounds[3],  # latency C
                    ]
                )

    logger.info("exported balanced Latin-square schedules to %s", csv_path)
