import logging
import pathlib
import pynput.mouse
from harness import logging as harness_logging

logger = logging.getLogger(__name__)


def on_move(x, y):
    logger.info("mouse moved to, {0}, {1}".format(x, y))


def on_click(x, y, button, pressed):
    if pressed:
        logger.info("mouse clicked at, {0}, {1}, {2}".format(x, y, button))


def on_scroll(x, y, dx, dy):
    logger.info("mouse scrolled at, {0}, {1}, {2}, {3}".format(x, y, dx, dy))


def start(log_path: str | pathlib.Path) -> pynput.mouse.Listener:
    harness_logging.configure_log_to_file(logger, log_path)
    thread = pynput.mouse.Listener(
        on_move=on_move, on_click=on_click, on_scroll=on_scroll
    )
    thread.start()
    return thread
