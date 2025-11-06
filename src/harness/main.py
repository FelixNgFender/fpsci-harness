import logging
import pathlib
import random
import shutil
from typing import TYPE_CHECKING

import pydantic_settings
import rich.logging
import rich.prompt

from harness import constants, settings, utils
from harness.flows import feeding_frenzy, fitts, thanks
from harness.monitoring import keyboard, mouse

if TYPE_CHECKING:
    import pynput

logger = logging.getLogger(__name__)


def configure_logging(log_settings: settings.MonitorSettings) -> None:
    logging.basicConfig(
        level=logging.DEBUG if log_settings.verbose else logging.INFO,
        format="%(message)s",
        handlers=[rich.logging.RichHandler(rich_tracebacks=True)],
    )
    logger.debug("running with settings %s", log_settings)


def start(start_settings: settings.StartSettings) -> None:
    """Randomize list of games in an experiment and match each with their respetive flow."""
    random.shuffle(start_settings.games) if start_settings.randomize_games else None
    random.shuffle(start_settings.latencies) if start_settings.randomize_latencies else None

    logger.debug("testing game list %s", start_settings.games)
    experiment_run_dir = start_settings.experiment_dir / utils.current_datetime_str()
    for g in start_settings.games:
        game_dir = experiment_run_dir / g
        ctx = settings.GameContext(**start_settings.model_dump(), game_dir=game_dir, game=g)
        pathlib.Path(ctx.game_dir).mkdir(parents=True, exist_ok=True)
        match g:
            case settings.Game.FITTS:
                fitts.start(ctx)
            case settings.Game.FEEDIND_FRENZY:
                feeding_frenzy.start(ctx)
            case _:
                msg = "unknown game"
                raise RuntimeError(msg)
    thanks.popup_thank_you_banner()


class Start(settings.StartSettings):
    """Runs the harness and collects the results."""

    def cli_cmd(self) -> None:
        configure_logging(self)
        start(self)


def monitor(monitor_settings: settings.MonitorSettings) -> None:
    monitoring_run_dir = monitor_settings.experiment_dir / utils.current_datetime_str()
    pathlib.Path(monitoring_run_dir).mkdir(parents=True, exist_ok=True)
    listeners: list[pynput.keyboard.Listener | pynput.mouse.Listener] = []
    match monitor_settings.monitor_choice:
        case settings.MonitoringChoice.ALL:
            listeners.append(keyboard.start(monitoring_run_dir / constants.KEYBOARD_LOG))
            listeners.append(mouse.start(monitoring_run_dir / constants.MOUSE_LOG))
        case settings.MonitoringChoice.KEYBOARD:
            listeners.append(keyboard.start(monitoring_run_dir / constants.KEYBOARD_LOG))
        case settings.MonitoringChoice.MOUSE:
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
    start: pydantic_settings.CliSubCommand[Start]
    monitor: pydantic_settings.CliSubCommand[Monitor]
    clean: pydantic_settings.CliSubCommand[Clean]

    def cli_cmd(self) -> None:
        pydantic_settings.CliApp.run_subcommand(self)


def main() -> None:
    pydantic_settings.CliApp.run(Command)


if __name__ == "__main__":
    main()
