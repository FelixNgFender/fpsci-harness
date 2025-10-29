import sys
import random
import time
import pyautogui
import os
from datetime import datetime
import shutil
from pywinauto.application import Application
from os import startfile
import subprocess
import webbrowser
import logging
import pathlib
import tkinter as tk
import tkinter.font as font
import harness.settings as settings
import harness.monitoring.config_logging as config_logging
import harness.process as process
import harness.flows.shared as shared_flow
import harness.constants as constants

logger = logging.getLogger(__name__)

# Testing flow

# 1. No need to open up the game
# 2. Generate a number from 0 to max benchmarks


def start(game_settings: settings.GameContext) -> None:
    """Announce Fitt's law game, play a tutorial video"""
    config_logging.configure(
        logger, game_settings.game_dir / f"{game_settings.game}.csv"
    )
    webbrowser.register(
        "browser",
        None,
        webbrowser.GenericBrowser(
            [
                str(constants.CHROME_PATH),
                "--incognito",
                "%s",
            ]
        ),
        preferred=True,
    )
    logger.debug("starting %s flow", str(game_settings.game))
    popup_start_banner()
    play_tutorial_video()
    play_test_round(game_settings.game_dir, game_settings.game_duration)
    for latency in game_settings.latencies:
        shared_flow.popup_next_round_banner()
        play_round(game_settings.game_dir, duration_s=game_settings.game_duration, latency=latency)


def popup_start_banner() -> None:
    """Display a banner announcing the start of the Fitts' Law game."""
    root = tk.Tk()
    root.title("Fitts' Law Experiment")
    root.configure(bg="#FFFFFF")
    root.geometry("500x300")
    root.resizable(False, False)

    # Custom fonts
    title_font = font.Font(family="Helvetica", size=22, weight="bold")
    subtitle_font = font.Font(family="Helvetica", size=12)

    # Title label
    tk.Label(
        root,
        text="Welcome to the Fitts' Law Game!",
        font=title_font,
        bg="#FFFFFF",
        fg="#003366",
    ).pack(pady=(50, 10))

    # Subtitle text
    tk.Label(
        root,
        text="Test your speed and accuracy.\nClick 'Start' to begin.",
        font=subtitle_font,
        bg="#FFFFFF",
        fg="#333333",
        justify="center",
    ).pack(pady=(0, 40))

    # Start button
    start_button = tk.Button(
        root,
        text="Start",
        font=("Helvetica", 14, "bold"),
        bg="#0078D7",
        fg="#FFFFFF",
        activebackground="#005A9E",
        activeforeground="#FFFFFF",
        relief="raised",
        width=12,
        height=2,
        command=root.destroy,  # closes the banner
        borderwidth=0,
    )
    start_button.pack()

    # Disable closing via the X button
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.mainloop()


def play_tutorial_video() -> None:
    """Play tutorial video and wait until close (since `startfile` returns immediately)"""
    process.play_valorant_tutorial()
    while process.is_media_player_alive():
        time.sleep(0.5)


def start_fitts_process() -> subprocess.Popen:
    return process.start_process(constants.FITTS_URL)


def play_test_round(game_dir: pathlib.Path, duration_s: int) -> None:
    fitts_subprocess = start_fitts_process()
    logger.info("starting test round")
    shared_flow.popup_test_round_start_banner()
    # playing
    time.sleep(duration_s)
    # TODO: do we need to collect any stats here?
    pyautogui.screenshot(game_dir / "test_round_end.png")
    shared_flow.popup_test_round_end_banner()
    logger.info("test round ended")
    fitts_subprocess.kill()


def play_round(game_dir: pathlib.Path, *, duration_s: int, latency: int) -> None:
    fitts_subprocess = start_fitts_process()
    logger.info("starting test round")
    shared_flow.popup_test_round_start_banner()
    # playing
    time.sleep(duration_s)
    # TODO: do we need to collect any stats here?
    pyautogui.screenshot(game_dir / "test_round_end.png")
    shared_flow.popup_test_round_end_banner()
    logger.info("test round ended")
    fitts_subprocess.kill()


# REPEAT = [0, 13, 14, 15]
# FRAMERATE = [60, 120]

# cond = [0, 1, 2, 3, 4, 5, 6]  # 4 constant + 3 chaos

# random.shuffle(cond)
# random.shuffle(REPEAT)
# random.shuffle(FRAMERATE)

# ind = 0
# # The first frame rate
# while count < 14:
#     # set frame rate
#     fr1 = FRAMERATE[0]
#     fr2 = FRAMERATE[1]

#     if count == 0:
#         if fr1 == 60:
#             os.system(
#                 'START "" "C:\\Program Files (x86)\\RivaTuner Statistics Server\\RTSS.exe"'
#             )
#         else:
#             os.system(
#                 'START "" "C:\\Program Files (x86)\\RivaTuner Statistics Server 120\\RTSS120.exe"'
#             )
#         log.write(
#             datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
#             + " "
#             + str(fr1)
#             + " fr "
#             + str(fr2)
#             + " fr\n"
#         )

#     if count == 7:  # next, restart game
#         ind = 0
#         kill_fitts()

#         if fr2 == 60:
#             kill_RTSS120()
#             start_fitts()
#             time.sleep(5)
#             os.system(
#                 'START "" "C:\\Program Files (x86)\\RivaTuner Statistics Server\\RTSS.exe"'
#             )
#             time.sleep(7)
#         else:
#             kill_RTSS()
#             start_fitts()
#             time.sleep(5)
#             os.system(
#                 'START "" "C:\\Program Files (x86)\\RivaTuner Statistics Server 120\\RTSS120.exe"'
#             )
#             time.sleep(7)

#     cur = cond[ind]
#     cur_benchmark = 0
#     if cur < 4:  # constant rounds
#         cur_benchmark = REPEAT[cur]
#         if cur_benchmark > 0:
#             fibo = "START  pythonw C:\\Users\\shengmei\\Desktop\\Flow\\Loops\\Fibo1.pyw"
#             for i in range(1, cur_benchmark + 1):
#                 os.system(fibo)
#     else:
#         if cur == 4:
#             cur_benchmark = 44
#             os.system(
#                 f'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw {1} {1.0} {2.0}'
#             )
#         elif cur == 5:
#             cur_benchmark = 55
#             os.system(
#                 f'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw {1} {0.25} {0.5}'
#             )
#         else:
#             cur_benchmark = 66
#             os.system(
#                 f'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw {2} {4.0} {6.0}'
#             )
#         # cmd = "START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw"
#         # os.system(cmd)
#     ## if we need to randomize
#     # condition = random.randint(1, 3)  #contant condition or variations
#     # cur_benchmark = 0
#     # if condition < 3: #constant condition
#     #     cur_benchmark = random.randint(min_benchmark, max_benchmark)
#     #     #run benchmarks
#     #
#     #     #fibo = "C:/Users/shengmei/Desktop/Flow/Loops/loop1.bat"
#     #     fibo = "START "" pythonw C:\\Users\\shengmei\\Desktop\\Flow\\Loops\\Fibo1.pyw"
#     #     for i in range(1, cur_benchmark + 1):
#     #         os.system(fibo)
#     # else:
#     #     cmd = "START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw"
#     #     os.system(cmd)

#     # call API to play game
#     log.write(
#         datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
#         + " "
#         + str(cur_benchmark)
#         + " benchmarks\n"
#     )
#     log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " game started\n")
#     log.write(
#         datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
#         + " Round "
#         + str(count)
#         + " \n"
#     )
#     set_focus()

#     # mouse and keyboard
#     cmd = 'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\keyboard.pyw'
#     os.system(cmd)

#     cmd = 'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\mouse.pyw'
#     os.system(cmd)

#     # presentMon
#     cmd = 'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\PresentMon.pyw'
#     os.system(cmd)

#     # game playing
#     time.sleep(60)

#     # game ending, kill benchmarks
#     # os.system("taskkill /f /im cmd.exe")
#     os.system("taskkill /f /im pythonw.exe")
#     # os.system("wmic process where \"name=\'PresentMon64-dev210107.exe\'\" delete")

#     # log performance
#     shutil.copy2(
#         scorePath,
#         f"C:\\Users\\shengmei\\Documents\\Score\\score{count}_{cur_benchmark}.log",
#     )
#     # myScreenshot = pyautogui.screenshot()
#     # myScreenshot.save(f'C:\\Users\\shengmei\\Documents\\Screenshots\\valorant_{count}_{cur_benchmark}.png')
#     log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " game ended\n")

#     # log mouse and keyboard
#     shutil.move(
#         "C:\\Users\\shengmei\\Documents\\mouse_log.txt",
#         f"C:\\Users\\shengmei\\Documents\\Evlog\\mouse_{count}_{cur_benchmark}.txt",
#     )
#     shutil.move(
#         "C:\\Users\\shengmei\\Documents\\keyboard_log.txt",
#         f"C:\\Users\\shengmei\\Documents\\Evlog\\keyboard_{count}_{cur_benchmark}.txt",
#     )

#     # PresentMon
#     time.sleep(2)
#     os.system("taskkill /f /im PresentMon64-dev210107.exe")
#     shutil.move(
#         "C:\\Users\\shengmei\\Documents\\PresentMon.csv",
#         f"C:\\Users\\shengmei\\Documents\\PresentMon\\PresentMon_{count}_{cur_benchmark}.csv",
#     )

#     # call API for QoE
#     cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\QoE\\QoE.py"
#     os.system(cmd)
#     log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " survey taken\n")

#     # Store the data from this round (we only need to move QoE data)
#     if os.path.exists("C:/Users/shengmei/Documents/QoE.txt"):
#         shutil.move(
#             "C:/Users/shengmei/Documents/QoE.txt",
#             f"C:/Users/shengmei/Documents/QoEs/QoE_{count}_{cur_benchmark}.txt",
#         )

#     if os.path.exists("C:/Users/shengmei/Documents/chaos.txt"):
#         shutil.move(
#             "C:/Users/shengmei/Documents/chaos.txt",
#             f"C:/Users/shengmei/Documents/Chaos/chaos_{count}_{cur_benchmark}.txt",
#         )

#     # Next round
#     cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\Next\\next.py"
#     os.system(cmd)
#     count = count + 1
#     ind = ind + 1
#     if count == 14:
#         if fr2 == 60:
#             kill_RTSS()
#         else:
#             kill_RTSS120()
# # terminate valorant and remove performance log
# os.system("taskkill /f /im VALORANT-Win64-Shipping.exe")
# time.sleep(2)
# # os.system("taskkill /f /im VALORANT.exe")
# shutil.move(scorePath, f"C:\\Users\\shengmei\\Documents\\Score\\score_all.log")
# log.close()

# # zip files (may change later)
# # filename = datetime.now().strftime("T-%d-%b-%Y-(%H-%M-%S-%f)")
# path = f"C:\\Users\\shengmei\\Documents\\Valorant"
# os.makedirs(path)
# shutil.move("C:\\Users\\shengmei\\Documents\\QoEs", path)
# shutil.move("C:\\Users\\shengmei\\Documents\\Score", path)
# shutil.move("C:\\Users\\shengmei\\Documents\\Evlog", path)
# shutil.move("C:\\Users\\shengmei\\Documents\\PresentMon", path)
# shutil.move("C:\\Users\\shengmei\\Documents\\Chaos", path)
# shutil.move("C:/Users/shengmei/Documents/scriptLogVa.txt", path)
# # shutil.move("C:\\Users\\shengmei\\Documents\\Screenshots", path)

# # shutil.make_archive(filename, 'zip', path)
# # log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " data archived")
# # log.close()

# # #Testing end window
# # cmd = 'python C:\\Users\\shengmei\\Desktop\\Flow\\Thanks\\thanks.py'
# # os.system(cmd)
