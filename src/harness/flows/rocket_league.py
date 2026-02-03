import logging
import pathlib
import shutil
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
        game_settings.game_dir / f"{game_settings.game_with_latencies.game}.stdout.csv",
    )
    logger.debug("starting %s flow", str(game_settings.game_with_latencies.game))
    start_game.popup_start_banner(
        window_title="Rocket League",
        title="Rocket League",
        description="TODO",
    )
    test_round_dir = game_settings.game_dir / f"{utils.get_current_datetime()}_test"
    pathlib.Path(test_round_dir).mkdir(parents=True, exist_ok=True)

    # preload and re-use game for all rounds
    subprocess.Popen(  # noqa: S603
        [constants.STEAM_ABSOLUTE_PATH, constants.ROCKET_LEAGUE_STEAM_APP_ID, *constants.ROCKET_LEAGUE_FLAGS]
    )

    play_round(
        test_round_dir,
        is_test=True,
        duration_s=game_settings.game_with_latencies.duration,
    )
    qoe.popup_qoe_questionnaire(test_round_dir / constants.QOE_ANSWERS)
    logger.info("qoe questionnaire taken")
    for latency_ms in game_settings.game_with_latencies.latencies:
        next_round.popup_next_round_banner()
        round_dir = game_settings.game_dir / f"{utils.get_current_datetime()}_{latency_ms}ms"
        pathlib.Path(round_dir).mkdir(parents=True, exist_ok=True)
        play_round(
            round_dir,
            duration_s=game_settings.game_with_latencies.duration,
            latency_ms=latency_ms,
        )
        qoe.popup_qoe_questionnaire(round_dir / constants.QOE_ANSWERS)
        logger.info("qoe questionnaire taken")

    process.kill_process_name(constants.ROCKET_LEAGUE_PROCESS)
    # at the end: batch convert replay files to json siblings using rrrocket.exe
    subprocess.run([constants.RRROCKET, "-m", str(game_settings.game_dir)], check=True)  # noqa: S603
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

    process.focus_window(constants.ROCKET_LEAGUE_WINDOW)

    while not is_in_menu():
        pyautogui.press("space", interval=0.5)
        continue

    # assume to be in menu right now - go into custom match - pause game
    pyautogui.click(172, 441, interval=0.2)  # enter play
    pyautogui.click(1400, 612, interval=0.2)  # enter private match
    pyautogui.click(741, 345, interval=0.2)  # enter create private match
    pyautogui.click(540, 797, interval=0.2)  # enter create match
    pyautogui.click(856, 650, interval=4)  # enter create match with password
    pyautogui.click(350, 375, interval=3)  # enter join orange
    time.sleep(3)  # match start time

    logger.info("starting test round" if is_test else "starting round")
    with monitoring.latency_context(results_dir, latency_ms):
        # wait until duration_s has elapsed
        time.sleep(duration_s)
        # collect stats
        with pyautogui.hold("tab"):
            time.sleep(0.2 + (latency_ms / 1000 if latency_ms else 0.0))
            pyautogui.screenshot(results_dir / constants.ROUND_END_SCREENSHOT)
            time.sleep(0.2)  # some tolerance

    logger.info("test round ended" if is_test else "round ended")
    logger.info("collected round result")

    # exit match, save replay and return to main menu
    pyautogui.press("esc", interval=1)  # pop up options
    pyautogui.click(975, 680, interval=0.2)  # enter leave match
    pyautogui.click(858, 617, interval=2)  # confirm leave match
    pyautogui.click(207, 695, interval=0.2)  # profile
    pyautogui.click(207, 645, interval=0.2)  # match history
    pyautogui.click(508, 394, interval=0.2)  # latest match
    pyautogui.click(352, 1023, interval=0.2)  # save replay
    pyautogui.typewrite(results_dir.name)  # replay name
    pyautogui.press("enter", interval=1)  # ok wait for replay to save
    pyautogui.press("esc", presses=10)  # back to menu
    # move replay from demo dir to results dir
    for replay in constants.ROCKET_LEAGUE_DEMO_DIR.glob("*.replay"):
        shutil.move(str(replay), str(results_dir / replay.name))
    if is_test:
        test_round.popup_test_round_end_banner()


def is_in_menu() -> bool:
    return pyautogui.pixelMatchesColor(537, 745, (254, 254, 254), tolerance=5) and pyautogui.pixelMatchesColor(
        1319, 514, (255, 255, 252), tolerance=5
    )
