import logging
import pathlib
import subprocess
import time
from collections.abc import Iterator

import pyautogui

from harness import constants, monitoring, process, settings, utils
from harness import logging as harness_logging
from harness.flows import next_round, qoe, start_game, test_round

logger = logging.getLogger(__name__)


def start(game_settings: settings.GameContext) -> None:
    """Run Rocket League rounds with optional latency injection and QoE prompts."""
    harness_logging.configure_log_to_file(
        logger,
        game_settings.game_dir / constants.ROCKET_LEAGUE_STDOUT,
    )
    logger.debug("starting %s flow", str(game_settings.game))

    # Show banner with tutorial (if file missing, VLC may fail but flow continues)
    start_game.popup_start_banner(
        window_title="Rocket League",
        title="Rocket League",
        description="Play a short round. Focus on normal gameplay.",
        tutorial_path=str(constants.ROCKET_LEAGUE_TUTORIAL_PATH),
    )

    # Test round first (no latency)
    test_round_dir = game_settings.game_dir / f"{utils.current_datetime_str()}_test"
    pathlib.Path(test_round_dir).mkdir(parents=True, exist_ok=True)
    play_round(
        test_round_dir,
        is_test=True,
        duration_s=game_settings.game_duration,
    )

    # Actual latency rounds
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
    """Launch Rocket League via Steam, wait, collect screenshot, and stop.

    Note: This is a minimal automation that launches the game, allows time for
    the participant to play, collects a screenshot, and then terminates the game.
    Further automation (e.g., navigating to Free Play, starting a custom match,
    or extracting in-game stats) can be layered on using image recognition.
    """
    steam_path = r"C:\Program Files (x86)\Steam\steam.exe"
    steam_app_id = "252950"  # Rocket League

    # Start Rocket League
    subprocess.Popen([steam_path, "-applaunch", steam_app_id], shell=False)  # noqa: S603
    logger.info("launched Rocket League via Steam")

    # Give time to load main menu
    _wait_with_spin(20)

    logger.info("starting test round" if is_test else "starting round")
    if is_test:
        test_round.popup_test_round_start_banner()

    # Optional: attempt a few ESC presses to bypass dialogs
    for _ in range(3):
        pyautogui.press("esc")
        time.sleep(0.5)

    with monitoring.latency_context(results_dir, latency_ms):
        # Let the participant play for the configured duration
        time.sleep(duration_s)
        # Capture an end-of-round screenshot for archival
        pyautogui.screenshot(results_dir / constants.ROUND_END_SCREENSHOT)

    logger.info("test round ended" if is_test else "round ended")
    _graceful_kill_game()

    if is_test:
        test_round.popup_test_round_end_banner()


def _graceful_kill_game() -> None:
    """Attempt to quit cleanly, then force kill."""
    # Try to open quit menu
    pyautogui.press("esc")
    time.sleep(0.5)
    pyautogui.press("esc")
    time.sleep(0.5)
    # Fall back to killing the process
    process.kill_process_name(constants.ROCKET_LEAGUE_PROCESS_NAME)


def _wait_with_spin(seconds: int) -> None:
    """Sleep helper that logs a simple countdown."""
    end_time = time.time() + seconds
    while time.time() < end_time:
        time.sleep(1)
