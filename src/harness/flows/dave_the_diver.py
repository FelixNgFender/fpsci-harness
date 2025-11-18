import logging
import pathlib
import subprocess
import time

import pyautogui
import pydirectinput
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
        window_title="Dave the Diver",
        title="Dave the Diver",
        description="TODO",
    )
    test_round_dir = game_settings.game_dir / f"{utils.current_datetime_str()}_test"
    pathlib.Path(test_round_dir).mkdir(parents=True, exist_ok=True)

    # preload and re-use game for all rounds
    subprocess.Popen(  # noqa: S603
        [
            constants.STEAM_ABSOLUTE_PATH,
            "-applaunch",
            constants.DAVE_THE_DIVER_STEAM_APP_ID,
            *constants.DAVE_THE_DIVER_FLAGS,
        ],
    )

    play_round(
        test_round_dir,
        duration_s=game_settings.game_duration,
        is_test=True,
        skip_menu=False,
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

    process.kill_process_name(constants.DAVE_THE_DIVER_PROCESS)
    logger.info("data archived")


def play_round(
    results_dir: pathlib.Path,
    *,
    duration_s: int,
    latency_ms: int | None = None,
    is_test: bool = False,
    skip_menu: bool = True,
) -> None:
    if is_test:
        test_round.popup_test_round_start_banner()

    process.focus_window(constants.DAVE_THE_DIVER_WINDOW)

    if not skip_menu:
        while is_not_in_menu():
            time.sleep(1)
            continue

        pydirectinput.press("space")  # continue

        while is_not_on_boat():
            time.sleep(0.1)
            continue

    pydirectinput.press("space", presses=10, interval=0.1)  # more than 2 for resiliency
    pydirectinput.keyDown("d")
    while is_not_in_position():
        continue
    pydirectinput.keyUp("d")

    pydirectinput.keyDown("space")
    while is_not_underwater():
        continue
    pydirectinput.keyUp("space")

    logger.info("starting test round" if is_test else "starting round")
    with monitoring.latency_context(results_dir, latency_ms):
        # wait until duration_s has elapsed
        time.sleep(duration_s)
        # collect stats
        pyautogui.screenshot(results_dir / constants.ROUND_END_SCREENSHOT)
        score_img = pyautogui.screenshot(region=(237, 972, 121, 34))
        score_img.save(results_dir / constants.DAVE_THE_DIVER_SCORE_IMG)

    logger.info("test round ended" if is_test else "round ended")
    score = pytesseract.image_to_string(score_img)
    pathlib.Path(results_dir / constants.DAVE_THE_DIVER_SCORE).write_text(score)
    logger.info("collected round result")

    # pause and return to boat
    while is_not_in_escape_menu():
        pydirectinput.press("esc", interval=0.1)
    pydirectinput.press("`")
    pydirectinput.keyDown("space")
    time.sleep(2)
    pydirectinput.keyUp("space")

    if is_test:
        test_round.popup_test_round_end_banner()


def is_not_in_menu() -> bool:
    return pyautogui.pixel(637, 366) != (253, 241, 0) and pyautogui.pixel(1176, 354) != (253, 241, 0)


def is_not_on_boat() -> bool:
    return pyautogui.pixel(216, 90) != (250, 118, 0) and pyautogui.pixel(168, 90) != (
        250,
        118,
        0,
    )


def is_not_in_position() -> bool:
    return pyautogui.pixel(939, 762) != (251, 199, 5) and pyautogui.pixel(778, 773) != (
        251,
        207,
        10,
    )


def is_not_underwater() -> bool:
    return pyautogui.pixel(166, 980) != (0, 174, 239) and pyautogui.pixel(91, 975) != (
        0,
        174,
        239,
    )


def is_not_in_escape_menu() -> bool:
    return pyautogui.pixel(166, 980) != (0, 42, 59) and pyautogui.pixel(91, 975) != (
        0,
        42,
        59,
    )
