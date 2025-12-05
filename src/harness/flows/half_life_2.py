import logging
import pathlib
import subprocess
import time

import pyautogui
import pydirectinput
import pytesseract
from fuzzywuzzy import fuzz

from harness import constants, monitoring, process, settings, utils
from harness import logging as harness_logging
from harness.flows import next_round, qoe, start_game, test_round

PARSE_THRESHOLD = 90
logger = logging.getLogger(__name__)


def start(game_settings: settings.GameContext) -> None:
    harness_logging.configure_log_to_file(
        logger,
        game_settings.game_dir / f"{game_settings.game}.stdout.csv",
    )
    logger.debug("starting %s flow", str(game_settings.game))
    start_game.popup_start_banner(
        window_title="Half-Life 2",
        title="Half-Life 2",
        description="TODO",
    )
    test_round_dir = game_settings.game_dir / f"{utils.current_datetime_str()}_test"
    pathlib.Path(test_round_dir).mkdir(parents=True, exist_ok=True)

    # preload and re-use game for all rounds
    subprocess.Popen(  # noqa: S603
        [
            constants.STEAM_ABSOLUTE_PATH,
            "-applaunch",
            constants.HALF_LIFE_2_STEAM_APP_ID,
            *constants.HALF_LIFE_2_FLAGS,
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

    process.kill_process_name(constants.HALF_LIFE_2_PROCESS)
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

    process.focus_window(constants.HALF_LIFE_2_WINDOW)

    if not skip_menu:
        while not is_workshop_window_open():
            pyautogui.typewrite("workshop_open_manager")
            pyautogui.press("enter")

        # while still in workshop, try to enter game until the workshop disappear
        while is_workshop_window_open():
            pyautogui.doubleClick(703, 392)
        time.sleep(5)  # entering game
    else:
        # resume from pause screen
        pydirectinput.press("`")

    logger.info("starting test round" if is_test else "starting round")
    with monitoring.latency_context(results_dir, latency_ms):
        # wait until duration_s has elapsed
        time.sleep(duration_s)

    logger.info("test round ended" if is_test else "round ended")

    # check if dump file exist so that can be used to dump later
    pathlib.Path(constants.HALF_LIFE_2_DUMP_PATH).unlink(missing_ok=True)
    pydirectinput.press("`")
    while not pathlib.Path(constants.HALF_LIFE_2_DUMP_PATH).exists():
        pyautogui.typewrite("condump")
        pyautogui.press("enter")

    # clear console text to not clutter other rounds
    pyautogui.typewrite("clear")
    pyautogui.press("enter")

    # parse score from dump
    with pathlib.Path(constants.HALF_LIFE_2_DUMP_PATH).open(encoding="utf-8") as f:
        score = sum(
            fuzz.ratio("Sending game message that npc_breen died to player", line.strip()) >= PARSE_THRESHOLD
            for line in f
        )
    pathlib.Path(results_dir / constants.HALF_LIFE_2_SCORE).write_text(str(score))
    pathlib.Path(constants.HALF_LIFE_2_DUMP_PATH).rename(results_dir / constants.HALF_LIFE_2_DUMP)
    logger.info("collected round result")

    if is_test:
        test_round.popup_test_round_end_banner()


def is_workshop_window_open() -> bool:
    workshop_title = pyautogui.screenshot(region=(653, 228, 95, 18))
    title = pytesseract.image_to_string(workshop_title).strip().lower()
    return "steam workshop" in title
