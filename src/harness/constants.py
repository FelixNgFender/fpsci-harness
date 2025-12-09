import pathlib

from harness import types

# General
DEFAULT_EXPERIMENT_PATH = pathlib.Path("experiment")
DEFAULT_LATENCIES = (0, 75, 150, 225)
DEFAULT_GAMES_WITH_LATENCIES: list[types.GameWithLatencies] = [
    types.GameWithLatencies(types.Game.FITTS, 30, DEFAULT_LATENCIES),
    types.GameWithLatencies(types.Game.FEEDING_FRENZY, 30, DEFAULT_LATENCIES),
    types.GameWithLatencies(types.Game.ROCKET_LEAGUE, 90, DEFAULT_LATENCIES),
    types.GameWithLatencies(types.Game.DAVE_THE_DIVER, 60, DEFAULT_LATENCIES),
    types.GameWithLatencies(types.Game.HALF_LIFE_2, 30, DEFAULT_LATENCIES),
]
DEFAULT_DURATION = 60
ASSETS_DIR = pathlib.Path("assets")
BACKUP_DIR = pathlib.Path.home() / "Documents" / "fpsci-2025-backup"
"""Contains tutorial videos and banner images"""
DATEFMT_STR = "%Y-%m-%d_%H-%M-%S"
STEAM_PROCESS = "steam.exe"
STEAM_ABSOLUTE_PATH = r"C:\Program Files (x86)\Steam\steam.exe"
EPIC_GAMES_PROCESS = "EpicGamesLauncher.exe"
EPIC_GAMES_ABSOLUTE_PATH = r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe"
RRROCKET = "rrrocket.exe"

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
ROCKET_LEAGUE_DEMO_DIR = pathlib.Path.home() / "Documents" / "My Games" / "Rocket League" / "TAGame" / "DemosEpic"
ROCKET_LEAGUE_PROCESS = "RocketLeague.exe"
ROCKET_LEAGUE_FLAGS = ["-nomovie"]
ROCKET_LEAGUE_WINDOW = "Rocket League (64-bit, DX11, Cooked)"

DAVE_THE_DIVER_STARTUP_TIMEOUT = 50
DAVE_THE_DIVER_STEAM_APP_ID = "1868140"
DAVE_THE_DIVER_FLAGS = ["-console", "-nomovie"]
DAVE_THE_DIVER_PROCESS = "DaveTheDiver.exe"
DAVE_THE_DIVER_WINDOW = "DAVE THE DIVER"
DAVE_THE_DIVER_SCORE_IMG = "score.png"
DAVE_THE_DIVER_SCORE = "score.txt"

HALF_LIFE_2_STEAM_APP_ID = "220"
HALF_LIFE_2_FLAGS = ["-console", "-novid"]
HALF_LIFE_2_PROCESS = "hl2.exe"
HALF_LIFE_2_WINDOW = "HALF-LIFE 2 - Direct3D 9"
HALF_LIFE_2_DUMP_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Half-Life 2\workshop\condump000.txt"
HALF_LIFE_2_DUMP = "dump.txt"
HALF_LIFE_2_SCORE = "score.txt"
