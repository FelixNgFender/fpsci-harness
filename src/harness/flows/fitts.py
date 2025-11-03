import os
import time
import pyautogui
import subprocess
import logging
import pathlib
from harness import settings
from harness import logging as harness_logging
from harness import process
from harness.flows import qoe
from harness.flows import start_game
from harness.flows import next_round
from harness.flows import test_round
from harness import constants
from harness import utils
from harness import monitoring

logger = logging.getLogger(__name__)


def start(game_settings: settings.GameContext) -> None:
    """Announce Fitt's law game, play a tutorial video, play the rounds with nvlatency"""
    harness_logging.configure_log_to_file(
        logger, game_settings.game_dir / f"{game_settings.game}.stdout.csv"
    )
    logger.debug("starting %s flow", str(game_settings.game))
    start_game.popup_start_banner(
        window_title="Fitts' Law Experiment",
        title="Welcome to the Fitts' Law Game!",
        description="Test your speed and accuracy.\nClick 'Start' to begin.",
        tutorial_path=str(constants.FITTS_TUTORIAL_PATH),
    )
    test_round_dir = game_settings.game_dir / f"{utils.current_datetime_str()}_test"
    os.makedirs(test_round_dir, exist_ok=True)
    play_round(
        test_round_dir,
        is_test=True,
        duration_s=game_settings.game_duration,
    )
    for latency_ms in game_settings.latencies:
        next_round.popup_next_round_banner()
        round_dir = (
            game_settings.game_dir / f"{utils.current_datetime_str()}_{latency_ms}ms"
        )
        os.makedirs(round_dir, exist_ok=True)
        play_round(
            round_dir,
            duration_s=game_settings.game_duration,
            latency_ms=latency_ms,
        )
        qoe.popup_qoe_questionnaire(round_dir / constants.QOE_ANSWERS)
        logger.info("qoe questionnaire taken")
    logger.info("data archived")


def start_fitts_process() -> subprocess.Popen:
    return process.start_process(constants.FITTS_URL)


def play_round(
    results_dir: pathlib.Path,
    *,
    duration_s: int,
    latency_ms: int | None = None,
    is_test: bool = False,
) -> None:
    # HACK: we cannot get a handle of a single chrome tab here so have to
    # kill all Chrome instances at the end
    start_fitts_process()
    logger.info("starting test round" if is_test else "starting round")
    if is_test:
        time.sleep(2)
        test_round.popup_test_round_start_banner()

    with monitoring.latency_context(results_dir, latency_ms):
        # playing
        time.sleep(duration_s)
        # TODO: do we need to collect any stats here?
        pyautogui.screenshot(
            results_dir
            / (
                constants.TEST_ROUND_END_SCREENSHOT
                if is_test
                else constants.ROUND_END_SCREENSHOT
            )
        )

    logger.info("test round ended" if is_test else "rounded ended")
    process.kill_chrome()
    if is_test:
        time.sleep(1)
        test_round.popup_test_round_end_banner()
