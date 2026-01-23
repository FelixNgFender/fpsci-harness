import contextlib
import os
import pathlib
import subprocess
import time

import pyautogui

from harness import constants


def process_exists(name: str) -> bool:
    """Return whether the process with the specified name exists."""
    call = "TASKLIST", "/FI", f"imagename eq {name}"
    # use built-in check_output right away
    output = subprocess.check_output(call).decode()  # noqa: S603
    # check in last line for process name
    last_line = output.strip().split("\r\n")[-1]
    # because Fail message could be translated and is cropped at 25 chars
    return last_line.lower()[:25].startswith(name.lower()[:25])


def kill_process_name(name: str) -> None:
    os.system(f"taskkill /f /im {name}")  # noqa: S605


def kill_process(p: subprocess.Popen) -> None:
    subprocess.check_call(["taskkill", "/F", "/T", "/PID", str(p.pid)])  # noqa: S603, S607


def focus_window(window_title: str, interval: float = 1) -> None:
    while True:
        with contextlib.suppress(IndexError):
            win = pyautogui.getWindowsWithTitle(window_title)[0]  # ty: ignore[unresolved-attribute]
            win.activate()
            return
        time.sleep(interval)


def start_nvlatency(
    latency_ms: int,
    stdout_log_path: str | pathlib.Path,
    stderr_log_path: str | pathlib.Path,
) -> subprocess.Popen:
    stdout_log_path = pathlib.Path(stdout_log_path)
    stderr_log_path = pathlib.Path(stderr_log_path)
    return subprocess.Popen(  # noqa: S603
        ["input-injector.exe", "--latency", "constant", str(latency_ms)],  # noqa: S607
        stdout=pathlib.Path.open(stdout_log_path, "a"),
        stderr=pathlib.Path.open(stderr_log_path, "a"),
    )


def start_steam_or_stop_if_not_exists() -> None:
    if not process_exists(constants.STEAM_PROCESS):
        subprocess.Popen([constants.STEAM_ABSOLUTE_PATH])  # noqa: S603
        msg = "Please tell developer to setup Steam"
        raise RuntimeError(msg)


def start_epic_games_or_stop_if_not_exists() -> None:
    if not process_exists(constants.EPIC_GAMES_PROCESS):
        subprocess.Popen([constants.EPIC_GAMES_ABSOLUTE_PATH])  # noqa: S603
        msg = "Please tell developer to setup Epic Games"
        raise RuntimeError(msg)
