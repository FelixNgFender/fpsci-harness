import pathlib

# General
DEFAULT_EXPERIMENT_PATH = pathlib.Path("experiment")
ASSETS_DIR = pathlib.Path("assets")
"""Contains tutorial videos and banner images"""
DATEFMT_STR = "%Y-%m-%d_%H-%M-%S"

# Experiment result artifact names
ROUND_END_SCREENSHOT = "round_end.png"
NVLATECY_STDOUT = "nvlatency.stdout.txt"
NVLATENCY_STDERR = "nvlatency.stderr.txt"
QOE_ANSWERS = "qoe.txt"
KEYBOARD_LOG = "kb.csv"
MOUSE_LOG = "mouse.csv"

# Shared assets
QOE_DIR = ASSETS_DIR / "qoe"
QOE_QUESTIONS = QOE_DIR / "questions.json"
QOE_CHART = QOE_DIR / "chart.jpg"

# Game-specific assets
FITTS_DIR = ASSETS_DIR / "fitts"
FITTS_ORIGINAL_RESULTS = "Fitts Law Experiment - Computer Science Field Guide.csv"
FITTS_RESULTS = "results.csv"
FITTS_TUTORIAL_PATH = FITTS_DIR / "tutorial.mp4"
FITTS_URL = "https://www.csfieldguide.org.nz/en/interactives/fitts-law/"
FITTS_DOWNLOAD_BTN_ID = "download-table-csv"
FITTS_RESTART_BTN_ID = "play-again"
