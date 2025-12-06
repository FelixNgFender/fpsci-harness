import enum
import pathlib
from typing import Annotated

import pydantic
import pydantic_settings

from harness import constants


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


class CleanSettings(pydantic_settings.BaseSettings):
    """Settings for the `clean` CLI subcommand."""

    experiment_dir: Annotated[
        pathlib.Path,
        pydantic.Field(description="Experiment results path to clean"),
    ] = constants.DEFAULT_EXPERIMENT_PATH
    force: Annotated[
        pydantic_settings.CliImplicitFlag[bool],
        pydantic.Field(description="Force clean without user confirmation (DANGEROUS)"),
    ] = False

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class LogSettings(pydantic_settings.BaseSettings):
    verbose: Annotated[
        pydantic_settings.CliImplicitFlag[bool],
        pydantic.Field(description="Logs extra debugging information"),
    ] = False
    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class MonitorSettings(LogSettings):
    """Settings for the `monitor` CLI subcommand."""

    monitor_choice: Annotated[
        MonitoringChoice,
        pydantic.Field(description="Which devices to monitor input for"),
    ] = MonitoringChoice.ALL
    monitor_duration: Annotated[
        int,
        pydantic.Field(description="Duration to monitor input devices (s)"),
    ] = constants.DEFAULT_DURATION
    experiment_dir: Annotated[
        pathlib.Path,
        pydantic.Field(description="Location to store experiment results"),
    ] = constants.DEFAULT_EXPERIMENT_PATH

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class ExperimentSettings(LogSettings):
    """Core experiment variables"""

    games: Annotated[
        list[Game],
        pydantic.Field(description="Games to test"),
    ] = list(Game)
    latencies: Annotated[
        list[int],
        pydantic.Field(description="Local latency levels to test (ms)"),
    ] = constants.DEFAULT_LATENCIES

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class StartSettings(ExperimentSettings, MonitorSettings):
    """Settings for the `start` CLI subcommand."""

    game_duration: Annotated[
        int,
        pydantic.Field(description="Duration of each game round (s)"),
    ] = constants.DEFAULT_DURATION

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class ConductSettings(StartSettings):
    """Settings for the `conduct` CLI subcommand."""

    input: Annotated[
        pathlib.Path | None,
        pydantic.Field(description="Location of the input schedule. `stdin` if not specified."),
    ] = None
    participant: Annotated[int, pydantic.Field(description="Participant ID in the schedule")]
    starting_game: Annotated[
        Game | None,
        pydantic.Field(
            description="Game at which this experiment should start at. Useful when restarting. "
            "Start at the beginning if null."
        ),
    ] = None

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class ScheduleSettings(ExperimentSettings):
    """Settings for the `schedule` CLI subcommand."""

    out: Annotated[
        pathlib.Path | None,
        pydantic.Field(description="Location to store the generated schedule. `stdout` if not specified."),
    ] = None

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class GameContext(StartSettings):
    """Add game-specific metadata to aid results tracking at runtime."""

    game_dir: Annotated[
        pathlib.Path,
        pydantic.Field(
            description="Directory to save experiment results for this game",
        ),
    ]
    game: Annotated[Game, pydantic.Field(description="The game being ran")]
