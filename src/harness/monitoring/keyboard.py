import logging
import pathlib
import pynput.keyboard
from harness import logging as harness_logging

logger = logging.getLogger(__name__)


def on_press(key):
    logging.info("kb pressed, {0}".format(key))


def on_release(key):
    logging.info("kb released, {0}".format(key))


def start(log_path: str | pathlib.Path) -> pynput.keyboard.Listener:
    harness_logging.configure_log_to_file(logger, log_path)
    thread = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
    thread.start()
    return thread
