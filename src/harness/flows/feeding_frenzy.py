import logging
import pathlib
import subprocess
import time

import pyautogui
import pytesseract

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
        window_title="Feeding Frenzy 2",
        title="Feeding Frenzy 2",
        description="TODO",
        tutorial_path=str(constants.FEEDING_FRENZY_TUTORIAL_PATH),
    )
    test_round_dir = game_settings.game_dir / f"{utils.current_datetime_str()}_test"
    pathlib.Path(test_round_dir).mkdir(parents=True, exist_ok=True)

    play_round(
        test_round_dir,
        is_test=True,
        duration_s=game_settings.game_duration,
    )
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

    logger.info("data archived")


def play_round(
    results_dir: pathlib.Path,
    *,
    duration_s: int,
    latency_ms: int | None = None,
    is_test: bool = False,
) -> None:
    if is_test:
        test_round.popup_test_round_start_banner()

    subprocess.Popen([constants.STEAM_ABSOLUTE_PATH, "-applaunch", "3390", "-fullscreen", "-novid"])  # noqa: S603
    while is_not_in_main_menu():
        continue

    pyautogui.moveTo(379, 241)
    pyautogui.click()

    while is_resume() and is_level():
        continue

    pyautogui.moveTo(400, 345)
    pyautogui.click()
    while is_level():
        continue

    pyautogui.moveTo(262, 129)
    pyautogui.click()

    pyautogui.moveTo(392, 542)
    while is_in_game():
        continue

    logger.info("starting test round" if is_test else "starting round")
    with monitoring.latency_context(results_dir, latency_ms):
        # wait until duration_s has elapsed
        time.sleep(duration_s)
        # collect stats
        pyautogui.screenshot(results_dir / constants.ROUND_END_SCREENSHOT)
        score_img = pyautogui.screenshot(region=(601, 5, 134, 31))
        score_img.save(results_dir / constants.FEEDING_FRENZY_SCORE_IMG)

    logger.info("test round ended" if is_test else "round ended")
    process.kill_process_name(constants.FEEDING_FRENZY_PROCESS)
    score = pytesseract.image_to_string(score_img)
    pathlib.Path(results_dir / constants.FEEDING_FRENZY_SCORE).write_text(score)
    logger.info("collected round result")
    if is_test:
        test_round.popup_test_round_end_banner()


def is_not_in_main_menu() -> bool:
    """Returns whether the player is NOT in the main menu of feeding frenzy"""
    return pyautogui.pixel(640, 507) != (117, 87, 35) and pyautogui.pixel(761, 505) != (
        128,
        102,
        51,
    )


def is_resume() -> bool:
    return pyautogui.pixel(272, 104) != (123, 94, 60) and pyautogui.pixel(526, 102) != (
        155,
        120,
        82,
    )


def is_level() -> bool:
    return pyautogui.pixel(35, 74) != (254, 247, 97) and pyautogui.pixel(137, 70) != (
        251,
        213,
        92,
    )


def is_in_game() -> bool:
    return pyautogui.pixel(299, 31) != (185, 143, 95) and pyautogui.pixel(529, 48) != (
        181,
        140,
        96,
    )
