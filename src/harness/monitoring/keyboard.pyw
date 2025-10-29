import logging
import time
import threading
import pynput.keyboard
import config_logging

logger = logging.getLogger(__name__)
config_logging.configure(logger, "./kb_log.txt")

def on_press(key):
    logging.info("Keyboard ({0}) pressed".format(key))

def on_release(key):
    logging.info("Keyboard ({0}) released".format(key))

def get_listener_thread() -> threading.Thread:
    return pynput.keyboard.Listener(on_press=on_press, on_release=on_release)