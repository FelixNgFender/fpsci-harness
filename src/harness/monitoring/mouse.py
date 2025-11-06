import logging
import pathlib

import pynput.mouse

from harness import logging as harness_logging

logger = logging.getLogger(__name__)


def on_move(x: int, y: int) -> bool | None:
    logger.info("mouse moved to, %s, %s", x, y)


def on_click(x: int, y: int, button: pynput.mouse.Button, pressed: bool) -> bool | None:  # noqa: FBT001
    if pressed:
        logger.info("mouse clicked at, %s, %s, %s", x, y, button)


def on_scroll(x: int, y: int, dx: int, dy: int) -> bool | None:
    logger.info("mouse scrolled at, %s, %s, %s, %s", x, y, dx, dy)


def start(log_path: str | pathlib.Path) -> pynput.mouse.Listener:
    harness_logging.configure_log_to_file(logger, log_path)
    thread = pynput.mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll,
    )
    thread.start()
    return thread
