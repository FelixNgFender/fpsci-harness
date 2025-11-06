import logging
import pathlib

import pyautogui
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions, ui

from harness import constants, monitoring, settings, utils
from harness import logging as harness_logging
from harness.flows import next_round, qoe, start_game, test_round

logger = logging.getLogger(__name__)


def start(game_settings: settings.GameContext) -> None:
    """Announce Fitt's law game, play a tutorial video, play the rounds with nvlatency."""
    harness_logging.configure_log_to_file(
        logger,
        game_settings.game_dir / f"{game_settings.game}.stdout.csv",
    )
    logger.debug("starting %s flow", str(game_settings.game))
    start_game.popup_start_banner(
        window_title="Fitts' Law Experiment",
        title="Welcome to the Fitts' Law Game!",
        description="Test your speed and accuracy.\nClick 'Start' to begin.",
        tutorial_path=str(constants.FITTS_TUTORIAL_PATH),
    )
    test_round_dir = game_settings.game_dir / f"{utils.current_datetime_str()}_test"
    pathlib.Path(test_round_dir).mkdir(parents=True, exist_ok=True)

    play_round(
        test_round_dir,
        is_test=True,
        duration_s=game_settings.game_duration,
    )
    for latency_ms in game_settings.latencies:
        next_round.popup_next_round_banner()
        round_dir = game_settings.game_dir / f"{utils.current_datetime_str()}_{latency_ms}ms"
        pathlib.Path(round_dir).mkdir(parents=True, exist_ok=True)
        play_round(
            round_dir,
            duration_s=game_settings.game_duration,
            latency_ms=latency_ms,
        )
        qoe.popup_qoe_questionnaire(round_dir / constants.QOE_ANSWERS)
        logger.info("qoe questionnaire taken")

    logger.info("data archived")


def play_round(
    results_dir: pathlib.Path,
    *,
    duration_s: int,
    latency_ms: int | None = None,
    is_test: bool = False,
) -> None:
    options = webdriver.ChromeOptions()
    options.add_argument("--kiosk")  # cannot exit with F11, requires Alt+F4 to close
    # disable the "Chrome is being controlled by automated test software" infobar
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # disable download dialogue and set default download dir
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": str(results_dir.resolve()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,  # ensures downloads are allowed
        },
    )
    driver = webdriver.Chrome(options=options)
    driver.get(constants.FITTS_URL)

    logger.info("starting test round" if is_test else "starting round")
    if is_test:
        test_round.popup_test_round_start_banner()

    with monitoring.latency_context(results_dir, latency_ms):
        # collect stats
        # wait until player is done or duration_s has elapsed, whichever comes first
        try:
            ui.WebDriverWait(driver, duration_s).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, constants.FITTS_DOWNLOAD_BTN_ID),
                ),
            ).click()
        except exceptions.TimeoutException:
            logger.warning("unfinished fitts round")
        pyautogui.screenshot(results_dir / constants.ROUND_END_SCREENSHOT)

    logger.info("test round ended" if is_test else "round ended")
    driver.quit()
    # rename results file if exists
    if (results_dir / constants.FITTS_ORIGINAL_RESULTS).exists():
        (results_dir / constants.FITTS_ORIGINAL_RESULTS).rename(
            results_dir / constants.FITTS_RESULTS,
        )
        logger.info("collected round result")
    if is_test:
        test_round.popup_test_round_end_banner()
