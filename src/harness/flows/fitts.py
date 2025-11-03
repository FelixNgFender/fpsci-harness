import os
import time
import pyautogui
import subprocess
import logging
import pathlib
import tkinter as tk
import tkinter.font as font
from harness import settings
from harness import logging as harness_logging
from harness import process
from harness.flows import qoe
from harness.flows import next_round
from harness.flows import test_round
from harness import constants
from harness import utils
from harness.monitoring import mouse
from harness.monitoring import keyboard

logger = logging.getLogger(__name__)


def start(game_settings: settings.GameContext) -> None:
    """Announce Fitt's law game, play a tutorial video, play the rounds with nvlatency"""
    harness_logging.configure_log_to_file(
        logger, game_settings.game_dir / f"{game_settings.game}.stdout.csv"
    )
    logger.debug("starting %s flow", str(game_settings.game))
    popup_start_banner()
    play_tutorial_video()
    current_datetime_str = utils.current_datetime_str()
    test_round_dir = game_settings.game_dir / f"{current_datetime_str}_test"
    os.makedirs(test_round_dir, exist_ok=True)
    play_round(
        test_round_dir,
        is_test=True,
        duration_s=game_settings.game_duration,
    )
    for latency_ms in game_settings.latencies:
        next_round.popup_next_round_banner()
        round_dir = game_settings.game_dir / f"{current_datetime_str}_{latency_ms}ms"
        os.makedirs(round_dir, exist_ok=True)
        play_round(
            round_dir,
            duration_s=game_settings.game_duration,
            latency_ms=latency_ms,
        )
        qoe.popup_qoe_questionnaire(round_dir / constants.QOE_ANSWERS)
        logger.info("qoe questionnaire taken")
    logger.info("data archived")


def popup_start_banner() -> None:
    """Display a banner announcing the start of the Fitts' Law game."""
    root = tk.Tk()
    root.title("Fitts' Law Experiment")
    root.configure(bg="#FFFFFF")
    root.attributes("-fullscreen", True)
    root.resizable(False, False)

    # Custom fonts
    title_font = font.Font(family="Helvetica", size=22, weight="bold")
    subtitle_font = font.Font(family="Helvetica", size=12)

    # Center container
    container = tk.Frame(root, bg="#FFFFFF")
    container.pack(expand=True)

    # Title label
    tk.Label(
        container,
        text="Welcome to the Fitts' Law Game!",
        font=title_font,
        bg="#FFFFFF",
        fg="#003366",
    ).pack(pady=(50, 10))

    # Subtitle text
    tk.Label(
        container,
        text="Test your speed and accuracy.\nClick 'Start' to begin.",
        font=subtitle_font,
        bg="#FFFFFF",
        fg="#333333",
        justify="center",
    ).pack(pady=(0, 40))

    # Start button
    start_button = tk.Button(
        container,
        text="Start",
        font=("Helvetica", 14, "bold"),
        bg="#0078D7",
        fg="#FFFFFF",
        activebackground="#005A9E",
        activeforeground="#FFFFFF",
        relief="raised",
        width=12,
        height=2,
        command=root.destroy,  # closes the banner
        borderwidth=0,
    )
    start_button.pack()

    # Disable closing via the X button
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.mainloop()


def play_tutorial_video() -> None:
    """Play tutorial video and wait until close (since `startfile` returns immediately)"""
    os.startfile(constants.FITTS_TUTORIAL_PATH)
    while process.is_media_player_alive():
        time.sleep(0.5)


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
    time.sleep(2)
    logger.info("starting test round" if is_test else "starting round")
    if is_test:
        test_round.popup_test_round_start_banner()
    else:
        test_round.popup_round_start_banner()
    if latency_ms is not None:
        kb_thread = keyboard.start(results_dir / constants.KEYBOARD_LOG)
        mouse_thread = mouse.start(results_dir / constants.MOUSE_LOG)
        if latency_ms != 0:
            nvlatency_process = process.start_nvlatency(
                latency_ms,
                results_dir / constants.NVLATECY_STDOUT,
                results_dir / constants.NVLATENCY_STDERR,
            )
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
    if is_test:
        test_round.popup_test_round_end_banner()
    else:
        test_round.popup_round_end_banner()
    logger.info("test round ended" if is_test else "rounded ended")
    process.kill_chrome()
    if latency_ms:
        if latency_ms != 0:
            nvlatency_process.kill()
        kb_thread.stop()
        mouse_thread.stop()
