import enum
import pathlib
from typing import Annotated

import pydantic
import pydantic_settings

from harness import constants


class Game(enum.StrEnum):
    """Add more games here."""

    FITTS = "fitts_law"
    FEEDIND_FRENZY = "feeding_frenzy"
    ROCKET_LEAGUE = "rocket_league"
    DAVE_THE_DIVER = "dave_the_diver"


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


class MonitorSettings(pydantic_settings.BaseSettings):
    """Settings for the `monitor` CLI subcommand."""

    verbose: Annotated[
        pydantic_settings.CliImplicitFlag[bool],
        pydantic.Field(description="Logs extra debugging information"),
    ] = False
    monitor_choice: Annotated[
        MonitoringChoice,
        pydantic.Field(description="Which devices to monitor input for"),
    ] = MonitoringChoice.ALL
    monitor_duration: Annotated[
        int,
        pydantic.Field(description="Duration to monitor input devices (s)"),
    ] = 60
    experiment_dir: Annotated[
        pathlib.Path,
        pydantic.Field(description="Location to store experiment results"),
    ] = constants.DEFAULT_EXPERIMENT_PATH

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class StartSettings(MonitorSettings):
    """Settings for latency experiment CLI."""

    games: Annotated[
        list[Game],
        pydantic.Field(description="Games to test"),
    ] = list(Game)
    game_duration: Annotated[
        int,
        pydantic.Field(description="Duration of each game round (s)"),
    ] = 60
    randomize_games: Annotated[
        pydantic_settings.CliImplicitFlag[bool],
        pydantic.Field(description="Whether to randomize game selection"),
    ] = True
    latencies: Annotated[
        list[int],
        pydantic.Field(description="Local latency levels to test (ms)"),
    ] = [0, 100, 500]
    randomize_latencies: Annotated[
        pydantic_settings.CliImplicitFlag[bool],
        pydantic.Field(description="Whether to randomize latencies"),
    ] = True

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
