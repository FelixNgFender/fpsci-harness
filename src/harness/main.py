import logging
import pathlib
import shutil
from typing import TYPE_CHECKING

import pydantic_settings
import rich.logging
import rich.prompt

from harness import constants, process, settings, types, utils
from harness import schedule as schedule_mod
from harness.flows import dave_the_diver, feeding_frenzy, fitts, half_life_2, rocket_league, thanks
from harness.monitoring import keyboard, mouse

if TYPE_CHECKING:
    import pynput

logger = logging.getLogger(__name__)


def configure_logging(log_settings: settings.LogSettings) -> None:
    logging.basicConfig(
        level=logging.DEBUG if log_settings.verbose else logging.INFO,
        format="%(message)s",
        handlers=[rich.logging.RichHandler(rich_tracebacks=True)],
    )
    logger.debug("running with settings %s", log_settings)


def start(start_settings: settings.StartSettings) -> None:
    """Match each game with their respetive flow."""
    process.start_epic_games_or_stop_if_not_exists()
    process.start_steam_or_stop_if_not_exists()

    logger.debug("testing game list %s", start_settings.games_with_latencies)
    experiment_run_dir = start_settings.experiment_dir / utils.current_datetime_str()
    for g in start_settings.games_with_latencies:
        game_dir = experiment_run_dir / g.game
        ctx = settings.GameContext(**start_settings.model_dump(), game_dir=game_dir, game_with_latencies=g)
        pathlib.Path(ctx.game_dir).mkdir(parents=True, exist_ok=True)
        match g.game:
            case types.Game.FITTS:
                fitts.start(ctx)
            case types.Game.FEEDING_FRENZY:
                feeding_frenzy.start(ctx)
            case types.Game.ROCKET_LEAGUE:
                rocket_league.start(ctx)
            case types.Game.DAVE_THE_DIVER:
                dave_the_diver.start(ctx)
            case types.Game.HALF_LIFE_2:
                half_life_2.start(ctx)
    thanks.popup_thank_you_banner()


class Start(settings.StartSettings):
    """Runs the harness and collects the results."""

    def cli_cmd(self) -> None:
        configure_logging(self)
        start(self)


def conduct(conduct_settings: settings.ConductSettings) -> None:
    schedule_obj = (
        schedule_mod.generate(conduct_settings.games_with_latencies)
        if conduct_settings.input is None
        else schedule_mod.Schedule.load_json(conduct_settings.input)
    )
    participant_schedule = schedule_obj.participants[conduct_settings.participant - 1]
    # start from starting game if specified
    if conduct_settings.starting_game is not None:
        games = [g.game for g in participant_schedule.games_with_latencies]
        participant_schedule.games_with_latencies = participant_schedule.games_with_latencies[
            games.index(conduct_settings.starting_game) :
        ]
    logger.info("conduting participant schedule %s", participant_schedule)

    process.start_epic_games_or_stop_if_not_exists()
    process.start_steam_or_stop_if_not_exists()
    current_dt = utils.current_datetime_str()
    experiment_run_dir = conduct_settings.experiment_dir / current_dt
    for g in participant_schedule.games_with_latencies:
        game_dir = experiment_run_dir / g.game
        raw = conduct_settings.model_dump()

        # remove conflicting keys
        raw.pop("games_with_latencies", None)
        ctx = settings.GameContext(
            **raw,
            games_with_latencies=participant_schedule.games_with_latencies,
            game_dir=game_dir,
            game_with_latencies=g,
        )
        pathlib.Path(ctx.game_dir).mkdir(parents=True, exist_ok=True)
        match g.game:
            case types.Game.FITTS:
                fitts.start(ctx)
            case types.Game.FEEDING_FRENZY:
                feeding_frenzy.start(ctx)
            case types.Game.ROCKET_LEAGUE:
                rocket_league.start(ctx)
            case types.Game.DAVE_THE_DIVER:
                dave_the_diver.start(ctx)
            case types.Game.HALF_LIFE_2:
                half_life_2.start(ctx)
    thanks.popup_thank_you_banner()

    # back up qoe data
    backup_dir = constants.BACKUP_DIR / str(participant_schedule.participant) / current_dt
    shutil.copytree(src=experiment_run_dir, dst=backup_dir)


class Conduct(settings.ConductSettings):
    """
    Conduct the experiment for a participant from a schedule. If `input` is not specified, generate a schedule.
    """

    def cli_cmd(self) -> None:
        configure_logging(self)
        conduct(self)


def schedule(schedule_settings: settings.ScheduleSettings) -> None:
    schedule_obj = schedule_mod.generate(schedule_settings.games_with_latencies)
    if schedule_settings.output is None:
        logger.info("generated schedule %s", schedule_obj)
        return

    with schedule_settings.output.open("w", newline="", encoding="utf-8") as f:
        schedule_obj.to_json(f)
    logger.info("exported schedule to %s", schedule_settings.output)


class Schedule(settings.ScheduleSettings):
    """Schedule mass experiment configurations using latin squares."""

    def cli_cmd(self) -> None:
        configure_logging(self)
        schedule(self)


def monitor(monitor_settings: settings.MonitorSettings) -> None:
    monitoring_run_dir = monitor_settings.experiment_dir / utils.current_datetime_str()
    pathlib.Path(monitoring_run_dir).mkdir(parents=True, exist_ok=True)
    listeners: list[pynput.keyboard.Listener | pynput.mouse.Listener] = []
    match monitor_settings.monitor_choice:
        case types.MonitoringChoice.ALL:
            listeners.append(keyboard.start(monitoring_run_dir / constants.KEYBOARD_LOG))
            listeners.append(mouse.start(monitoring_run_dir / constants.MOUSE_LOG))
        case types.MonitoringChoice.KEYBOARD:
            listeners.append(keyboard.start(monitoring_run_dir / constants.KEYBOARD_LOG))
        case types.MonitoringChoice.MOUSE:
            listeners.append(mouse.start(monitoring_run_dir / constants.MOUSE_LOG))

    logger.info("Listener(s) running. Kill the currently running terminal if you want to stop.")
    for listener in listeners:
        listener.join()  # Blocks


class Monitor(settings.MonitorSettings):
    """Runs monitoring tools without running the games like the `start` command."""

    def cli_cmd(self) -> None:
        configure_logging(self)
        monitor(self)


class Clean(settings.CleanSettings):
    """Cleans experiment results directory."""

    def cli_cmd(self) -> None:
        if self.force or rich.prompt.Confirm.ask(
            f"Delete the experiment results folder located at `{self.experiment_dir}`? THIS ACTION IS NOT REVERSIBLE.",
            default=False,
        ):
            shutil.rmtree(self.experiment_dir)


class Command(
    pydantic_settings.BaseSettings,
    cli_parse_args=True,
    cli_use_class_docs_for_groups=True,
    cli_kebab_case=True,
):
    """Harness for conducting experiments for WPI FPSci IQP 2025"""

    start: pydantic_settings.CliSubCommand[Start]
    conduct: pydantic_settings.CliSubCommand[Conduct]
    schedule: pydantic_settings.CliSubCommand[Schedule]
    monitor: pydantic_settings.CliSubCommand[Monitor]
    clean: pydantic_settings.CliSubCommand[Clean]

    def cli_cmd(self) -> None:
        pydantic_settings.CliApp.run_subcommand(self)


def main() -> None:
    pydantic_settings.CliApp.run(Command)


if __name__ == "__main__":
    main()
