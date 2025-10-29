import pathlib

# General
DEFAULT_EXPERIMENT_PATH = pathlib.Path("experiment")
ASSETS_DIR = pathlib.Path("assets")
"""Contains tutorial videos and banner images"""
MEDIA_PLAYER_PROCESS_NAME = "Microsoft.Media.Player.exe"
CHROME_PATH = pathlib.Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

# Game-specific
FITTS_DIR = ASSETS_DIR / "fitts"
FITTS_TUTORIAL_PATH = FITTS_DIR / "tutorial.mp4"
FITTS_URL = "https://www.csfieldguide.org.nz/en/interactives/fitts-law/"
