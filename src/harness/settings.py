import pathlib
from typing import Annotated

import pydantic
import pydantic_settings

from harness import constants, types


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
    experiment_dir: Annotated[
        pathlib.Path,
        pydantic.Field(description="Location to store experiment results"),
    ] = constants.DEFAULT_EXPERIMENT_PATH

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class MonitorSettings(LogSettings):
    """Settings for the `monitor` CLI subcommand."""

    monitor_choice: Annotated[
        types.MonitoringChoice,
        pydantic.Field(description="Which devices to monitor input for"),
    ] = types.MonitoringChoice.ALL
    monitor_duration: Annotated[
        int,
        pydantic.Field(description="Duration to monitor input devices (s)"),
    ] = constants.DEFAULT_DURATION

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class ExperimentSettings(LogSettings):
    """Core experiment variables"""

    games_with_latencies: Annotated[
        list[types.GameWithLatencies],
        pydantic.Field(description="Games with their respective latencies to test"),
    ] = constants.DEFAULT_GAMES_WITH_LATENCIES

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class StartSettings(ExperimentSettings, MonitorSettings):
    """Settings for the `start` CLI subcommand."""

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class ConductSettings(StartSettings):
    """Settings for the `conduct` CLI subcommand."""

    input: Annotated[
        pathlib.Path | None,
        pydantic.Field(
            description="Location of the input schedule. Use `harness schedule` to generate an in-memory "
            "schedule if this is not specified."
        ),
    ] = None
    participant: Annotated[int, pydantic.Field(description="Participant ID to run schedule for")]
    starting_game: Annotated[
        types.Game | None,
        pydantic.Field(
            description="Game at which this experiment should start at. Useful when restarting. "
            "Start at the beginning if null."
        ),
    ] = None

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env", extra="ignore")


class ScheduleSettings(ExperimentSettings):
    """Settings for the `schedule` CLI subcommand."""

    output: Annotated[
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
    game_with_latencies: Annotated[
        types.GameWithLatencies, pydantic.Field(description="The game being ran with its configured latencies")
    ]
