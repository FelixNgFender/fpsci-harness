import logging
import pathlib
import subprocess
import time

import pyautogui

from harness import constants, monitoring, process, settings, utils
from harness import logging as harness_logging
from harness.flows import next_round, qoe, start_game, test_round

logger = logging.getLogger(__name__)


def start(game_settings: settings.GameContext) -> None:
    harness_logging.configure_log_to_file(
        logger,
        game_settings.game_dir / f"{game_settings.game}.stdout.csv",
    )
    logger.debug("starting %s flow", str(game_settings.game))
    start_game.popup_start_banner(
        window_title="Rocket League",
        title="Rocket League",
        description="TODO",
    )
    test_round_dir = game_settings.game_dir / f"{utils.current_datetime_str()}_test"
    pathlib.Path(test_round_dir).mkdir(parents=True, exist_ok=True)

    # preload and re-use game for all rounds
    subprocess.Popen([constants.STEAM_ABSOLUTE_PATH, constants.ROCKET_LEAGUE_STEAM_APP_ID, "-nomovie"])  # noqa: S603
    time.sleep(constants.ROCKET_LEAGUE_STARTUP_TIME_S)
    pyautogui.press("enter")  # enter menu
    time.sleep(0.5)

    play_round(
        test_round_dir,
        is_test=True,
        duration_s=game_settings.game_duration,
    )
    qoe.popup_qoe_questionnaire(test_round_dir / constants.QOE_ANSWERS)
    logger.info("qoe questionnaire taken")
    for latency_ms in game_settings.latencies:
        next_round.popup_next_round_banner()
        round_dir = game_settings.game_dir / f"{utils.current_datetime_str()}_{latency_ms}ms"
        pathlib.Path(round_dir).mkdir(parents=True, exist_ok=True)
        play_round(
            round_dir,
            duration_s=game_settings.game_duration,
            latency_ms=latency_ms,
        )
        qoe.popup_qoe_questionnaire(round_dir / constants.QOE_ANSWERS)
        logger.info("qoe questionnaire taken")

    process.kill_process_name(constants.ROCKET_LEAGUE_PROCESS)
    # TODO: at the end: batch convert replay file to json using rrrocket.exe
    # .\rrrocket.exe -m .\experiment\2025-11-10_21-17-30\rocket_league\
    logger.info("data archived")


def play_round(
    results_dir: pathlib.Path,
    *,
    duration_s: int,
    latency_ms: int | None = None,
    is_test: bool = False,
) -> None:
    # assume to be in menu right now - go into custom match - pause game
    pyautogui.press("right")
    pyautogui.press("enter")  # enter play
    time.sleep(0.5)
    pyautogui.press("right")
    pyautogui.press("enter")  # enter private match
    time.sleep(0.5)
    pyautogui.press("up")
    pyautogui.press("up")
    pyautogui.press("enter")  # enter create private match
    time.sleep(0.5)
    pyautogui.press("up")
    pyautogui.press("down")
    pyautogui.press("enter")  # enter create match
    pyautogui.press("down")
    pyautogui.press("down")
    pyautogui.press("enter")  # enter create match with password
    time.sleep(3)  # entering match
    pyautogui.press("down")
    pyautogui.press("enter")  # enter join orange
    time.sleep(5)
    pyautogui.press("esc")
    pyautogui.press("down")
    pyautogui.press("enter")  # enter pause game

    if is_test:
        test_round.popup_test_round_start_banner()

    logger.info("starting test round" if is_test else "starting round")
    with monitoring.latency_context(results_dir, latency_ms):
        # wait until duration_s has elapsed
        time.sleep(duration_s)
        # collect stats
        with pyautogui.hold("tab"):
            pyautogui.screenshot(results_dir / constants.ROUND_END_SCREENSHOT)

    logger.info("test round ended" if is_test else "round ended")
    # TODO: move replay from constants.ROCKET_LEAGUE_DEMO_DIR to results_dir
    logger.info("collected round result")

    # pause and quit match to main menu
    pyautogui.press("esc")  # pop up options
    pyautogui.press("up")
    pyautogui.press("enter")  # enter leave match
    pyautogui.press("left")
    pyautogui.press("enter")  # confirm leave match

    if is_test:
        test_round.popup_test_round_end_banner()
