import ctypes
import logging
import pathlib

import pynput.keyboard

from harness import logging as harness_logging

PROCESS_PER_MONITOR_DPI_AWARE = 2

# https://pypi.org/project/pynput/#ensuring-consistent-coordinates-between-listener-and-controller-on-windows
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
logger = logging.getLogger(__name__)


def on_press(key: pynput.keyboard.Key | pynput.keyboard.KeyCode | None) -> None:
    logger.info("kb pressed, %s", key)


def on_release(key: pynput.keyboard.Key | pynput.keyboard.KeyCode | None) -> None:
    logger.info("kb released, %s", key)


def start(log_path: str | pathlib.Path) -> pynput.keyboard.Listener:
    harness_logging.configure_log_to_file(logger, log_path)
    thread = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
    thread.start()
    return thread
