from pynput.mouse import Listener
import pynput.mouse
import pynput.keyboard
import logging
import time
import config_logging

logger = logging.getLogger(__name__)
config_logging.configure(logger, "./mouse_log.txt")

def on_move(x, y):
    logger.info("Mouse moved to ({0}, {1})".format(x, y))

def on_click(x, y, button, pressed):
    if pressed:
        logger.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    logger.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

def get_listener_thread() -> threading.Thread:
    return pynput.mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
