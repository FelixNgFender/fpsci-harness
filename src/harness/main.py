import random
import os
from datetime import datetime
import shutil
import logging
import pydantic_settings
import rich.logging
import rich.prompt
from harness import settings
from harness import utils
from harness.flows import fitts

logger = logging.getLogger(__name__)


def configure_logging(log_settings: settings.MonitorSettings) -> None:
    logging.basicConfig(
        level=logging.DEBUG if log_settings.verbose else logging.INFO,
        format="%(message)s",
        handlers=[rich.logging.RichHandler(rich_tracebacks=True)],
    )
    logger.debug("running with settings %s", log_settings)


def start(start_settings: settings.StartSettings) -> None:
    """Randomize list of games in an experiment and match each with their respetive flow"""
    random.shuffle(start_settings.games) if start_settings.randomize_games else None
    random.shuffle(
        start_settings.latencies
    ) if start_settings.randomize_latencies else None

    logger.debug("testing game list %s", start_settings.games)
    experiment_run_dir = start_settings.experiment_dir / utils.current_datetime_str()
    for g in start_settings.games:
        game_dir = experiment_run_dir / g
        ctx = settings.GameContext(
            **start_settings.model_dump(), game_dir=game_dir, game=g
        )
        os.makedirs(ctx.game_dir, exist_ok=True)
        match g:
            case settings.Game.FITTS:
                fitts.start(ctx)
            case _:
                raise RuntimeError("unknown game")


# # #Testing end window
# # cmd = 'python C:\\Users\\shengmei\\Desktop\\Flow\\Thanks\\thanks.py'
# # os.system(cmd)


def _synthesize():
    path1 = "C:\\Users\\shengmei\\Documents\\Strange"
    path2 = "C:\\Users\\shengmei\\Documents\\Valorant"
    path3 = "C:\\Users\\shengmei\\Documents\\Rocket"
    filename = datetime.now().strftime("T-%d-%b-%Y-(%H-%M-%S-%f)")
    finalPath = f"C:\\Users\\shengmei\\Documents\\{filename}"
    os.makedirs(finalPath)
    shutil.move(path1, finalPath)
    shutil.move(path2, finalPath)
    shutil.move(path3, finalPath)
    shutil.make_archive(filename, "zip", finalPath)
    os.system("python C:\\Users\\shengmei\\Desktop\\Flow\\Thanks\\thanks.py")


class Start(settings.StartSettings):
    """Runs the harness and collects the results"""

    def cli_cmd(self) -> None:
        configure_logging(self)
        start(self)


class Monitor(settings.MonitorSettings):
    """Runs monitoring tools without running the games like the `start` command"""

    def cli_cmd(self) -> None:
        configure_logging(self)
        match self.monitor_choice:
            case settings.MonitoringChoice.ALL:
                pass
            case settings.MonitoringChoice.KEYBOARD:
                pass
            case settings.MonitoringChoice.MOUSE:
                pass
            case _:
                raise RuntimeError("unknown monitoring choice")


class Clean(settings.CleanSettings):
    """Cleans experiment results directory"""

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
