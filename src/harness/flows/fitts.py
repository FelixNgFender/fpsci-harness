import logging
import pathlib
import time
import urllib.parse

import jinja2
import pyautogui
from selenium import webdriver

from harness import constants, monitoring, settings, utils
from harness import logging as harness_logging
from harness.flows import next_round, qoe, start_game, test_round

logger = logging.getLogger(__name__)
env = jinja2.Environment(loader=jinja2.FileSystemLoader(constants.FITTS_DIR), autoescape=True)
fitts_html = env.get_template(constants.FITTS_HTML_TEMPLATE)


def start(game_settings: settings.GameContext) -> None:
    """Announce Fitt's law game, play a tutorial video, play the rounds with nvlatency."""
    harness_logging.configure_log_to_file(
        logger,
        game_settings.game_dir / f"{game_settings.game_with_latencies.game}.stdout.csv",
    )
    logger.debug("starting %s flow", str(game_settings.game_with_latencies.game))
    start_game.popup_start_banner(
        window_title="Fitts' Law Experiment",
        title="Welcome to the Fitts' Law Game!",
        description="Test your speed and accuracy.\nClick 'Start' to begin.",
    )
    test_round_dir = game_settings.game_dir / f"{utils.get_current_datetime()}_test"
    pathlib.Path(test_round_dir).mkdir(parents=True, exist_ok=True)

    play_round(
        test_round_dir,
        is_test=True,
        duration_s=game_settings.game_with_latencies.duration,
    )
    qoe.popup_qoe_questionnaire(test_round_dir / constants.QOE_ANSWERS)
    logger.info("qoe questionnaire taken")
    for latency_ms in game_settings.game_with_latencies.latencies:
        next_round.popup_next_round_banner()
        round_dir = game_settings.game_dir / f"{utils.get_current_datetime()}_{latency_ms}ms"
        pathlib.Path(round_dir).mkdir(parents=True, exist_ok=True)
        play_round(
            round_dir,
            duration_s=game_settings.game_with_latencies.duration,
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
    if is_test:
        test_round.popup_test_round_start_banner()

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
    html_content = fitts_html.render(time_limit=duration_s)
    encoded = urllib.parse.quote(html_content)
    driver.get(f"data:text/html;charset=utf-8,{encoded}")

    logger.info("starting test round" if is_test else "starting round")
    with monitoring.latency_context(results_dir, latency_ms):
        time.sleep(duration_s)
        time.sleep(1)  # make sure downloads go through
        pyautogui.screenshot(results_dir / constants.ROUND_END_SCREENSHOT)

    logger.info("test round ended" if is_test else "round ended")
    driver.quit()
    # rename results file if exists
    matches = list(results_dir.glob(constants.FITTS_ORIGINAL_RESULTS_REGEX))
    if matches:
        src = matches[0]
        dst = results_dir / constants.FITTS_RESULTS
        src.rename(dst)
        logger.info("collected round result from %s", src.name)
    else:
        logger.warning("no CSV result file found")
