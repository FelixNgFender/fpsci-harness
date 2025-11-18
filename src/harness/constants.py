import pathlib

# General
DEFAULT_EXPERIMENT_PATH = pathlib.Path("experiment")
ASSETS_DIR = pathlib.Path("assets")
"""Contains tutorial videos and banner images"""
DATEFMT_STR = "%Y-%m-%d_%H-%M-%S"
STEAM_PROCESS = "steam.exe"
STEAM_ABSOLUTE_PATH = r"C:\Program Files (x86)\Steam\steam.exe"
EPIC_GAMES_PROCESS = "EpicGamesLauncher.exe"
EPIC_GAMES_ABSOLUTE_PATH = r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe"

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
FITTS_ORIGINAL_RESULTS_REGEX = "fitts_per_click_*.csv"
FITTS_RESULTS = "results.csv"
FITTS_HTML_TEMPLATE = "index.jinja"
FITTS_DOWNLOAD_BTN_ID = "btn-download"

FEEDING_FRENZY_STEAM_APP_ID = "3390"
FEEDING_FRENZY_FLAGS = ["-fullscreen", "-novid"]
FEEDING_FRENZY_PROCESS = "popcapgame1.exe"
FEEDING_FRENZY_SCORE_IMG = "score.png"
FEEDING_FRENZY_SCORE = "score.txt"

ROCKET_LEAGUE_STEAM_APP_ID = "steam://rungameid/15938706871955750912"
ROCKET_LEAGUE_DEMO_DIR = r"C:\Users\shengmei\Documents\My Games\Rocket League\TAGame\DemosEpic"
ROCKET_LEAGUE_PROCESS = "RocketLeague.exe"
ROCKET_LEAGUE_FLAGS = ["-nomovie"]
ROCKET_LEAGUE_STARTUP_TIME_S = 18

DAVE_THE_DIVER_STARTUP_TIMEOUT = 50
DAVE_THE_DIVER_STEAM_APP_ID = "1868140"
DAVE_THE_DIVER_FLAGS = ["-console", "-nomovie"]
DAVE_THE_DIVER_PROCESS = "DaveTheDiver.exe"
DAVE_THE_DIVER_WINDOW = "DAVE THE DIVER"
DAVE_THE_DIVER_SCORE_IMG = "score.png"
DAVE_THE_DIVER_SCORE = "score.txt"
