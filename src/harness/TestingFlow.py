import random
import time
import pyautogui
import os
from datetime import datetime
import shutil
from pywinauto.application import Application
from os import startfile
import subprocess

import sys
# Testing flow

# 1. No need to open up the game
# 2. Generate a number from 0 to max benchmarks


def process_exists(process_name):
    call = "TASKLIST", "/FI", "imagename eq %s" % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split("\r\n")[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())


def set_focus():
    # app = Application().connect(title_re='VALORANT  ')
    # app['VALORANT  '].set_focus()
    pyautogui.click(x=610, y=1052, clicks=1, interval=0, button="left")


def start_valorant():
    pyautogui.doubleClick(x=110, y=135)
    pyautogui.FAILSAFE = False
    pyautogui.doubleClick(x=110, y=135)
    time.sleep(22)
    pyautogui.click(x=923, y=10, clicks=1, interval=0, button="left")
    # pyautogui.click(x=1240, y=30, clicks=1, interval=0, button='left')
    time.sleep(2)
    pyautogui.click(x=640, y=979, clicks=1, interval=0, button="left")
    # pyautogui.click(x=840, y=1315, clicks=1, interval=0, button='left')
    time.sleep(2)
    # pyautogui.click(x=1508, y=710, clicks=3, interval=0.3, button='middle')
    # pyautogui.click(x=1508, y=710, clicks=3, interval=0.3, button='middle')
    pyautogui.click(x=1124, y=508, clicks=3, interval=0.3, button="middle")
    pyautogui.click(x=1124, y=508, clicks=3, interval=0.3, button="middle")
    pyautogui.click(x=1124, y=508, clicks=3, interval=0.3, button="left")

    time.sleep(2)
    pyautogui.click(x=930, y=758, clicks=3, interval=0.3, button="right")
    pyautogui.click(x=930, y=758, clicks=3, interval=0.3, button="left")
    time.sleep(10)
    # pyautogui.click(x=1240, y=1015, clicks=3, interval=0.3, button='right')
    #
    # pyautogui.click(x=1240, y=1015, clicks=3, interval=0.3, button='left')


def kill_RTSS120():
    os.system("wmic process where \"name='RTSS120.exe'\" delete")
    os.system("wmic process where \"name='EncoderServer.exe'\" delete")
    os.system("wmic process where \"name='RTSSHooksLoader64.exe'\" delete")


def kill_RTSS():
    os.system("wmic process where \"name='RTSS.exe'\" delete")
    os.system("wmic process where \"name='EncoderServer.exe'\" delete")
    os.system("wmic process where \"name='RTSSHooksLoader64.exe'\" delete")


# Name of the next game
cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\valorant\\valorant.py"
os.system(cmd)

# play video and wait until close
startfile("C:\\Users\\shengmei\\Desktop\\Flow\\Valorant.mp4")
while process_exists("Video.UI.exe"):
    time.sleep(2)

# start valorant
start_valorant()

min_benchmark = 0
max_benchmark = 10

count = 0

# create folders for screenshots (performance) and QoE
if not os.path.exists("C:\\Users\\shengmei\\Documents\\Score"):
    os.makedirs("C:\\Users\\shengmei\\Documents\\Score")

if not os.path.exists("C:\\Users\\shengmei\\Documents\\QoEs"):
    os.makedirs("C:\\Users\\shengmei\\Documents\\QoEs")

if not os.path.exists("C:\\Users\\shengmei\\Documents\\Evlog"):
    os.makedirs("C:\\Users\\shengmei\\Documents\\Evlog")

if not os.path.exists("C:\\Users\\shengmei\\Documents\\PresentMon"):
    os.makedirs("C:\\Users\\shengmei\\Documents\\PresentMon")

Chaos = "C:\\Users\\shengmei\\Documents\\Chaos"
if not os.path.exists(Chaos):
    os.makedirs(Chaos)

scorePath = "C:\\Users\\shengmei\\AppData\\Local\VALORANT\\Saved\\Logs\\ShooterGame.log"


# scriptLog
log = open("C:/Users/shengmei/Documents/scriptLogVa.txt", "a")

log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " : Valorant time\n")
log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " : Test round\n")

# Test round first
# call API to play game
cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\Test\\test.py"
os.system(cmd)
set_focus()

# playing
time.sleep(60)
# myScreenshot = pyautogui.screenshot()
# myScreenshot.save(f'C:\\Users\\shengmei\\Documents\\Screenshots\\valorant_Test.png')

# cmd = 'python C:\\Users\\shengmei\\Desktop\\Flow\\Testend\\testend.py'
# os.system(cmd)
log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " : Test round ended\n")

cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\Next\\next.py"
os.system(cmd)

# No QoE for test round
# Test round ended API
REPEAT = [0, 13, 14, 15]
FRAMERATE = [60, 120]

cond = [0, 1, 2, 3, 4, 5, 6]  # 4 constant + 3 chaos

random.shuffle(cond)
random.shuffle(REPEAT)
random.shuffle(FRAMERATE)

ind = 0
# The first frame rate
while count < 14:
    # set frame rate
    fr1 = FRAMERATE[0]
    fr2 = FRAMERATE[1]

    if count == 0:
        if fr1 == 60:
            os.system(
                'START "" "C:\\Program Files (x86)\\RivaTuner Statistics Server\\RTSS.exe"'
            )
        else:
            os.system(
                'START "" "C:\\Program Files (x86)\\RivaTuner Statistics Server 120\\RTSS120.exe"'
            )
        log.write(
            datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            + " "
            + str(fr1)
            + " fr "
            + str(fr2)
            + " fr\n"
        )

    if count == 7:  # next, restart game
        ind = 0
        os.system("taskkill /f /im VALORANT-Win64-Shipping.exe")

        if fr2 == 60:
            kill_RTSS120()
            start_valorant()
            time.sleep(5)
            os.system(
                'START "" "C:\\Program Files (x86)\\RivaTuner Statistics Server\\RTSS.exe"'
            )
            time.sleep(7)
        else:
            kill_RTSS()
            start_valorant()
            time.sleep(5)
            os.system(
                'START "" "C:\\Program Files (x86)\\RivaTuner Statistics Server 120\\RTSS120.exe"'
            )
            time.sleep(7)

    cur = cond[ind]
    cur_benchmark = 0
    if cur < 4:  # constant rounds
        cur_benchmark = REPEAT[cur]
        if cur_benchmark > 0:
            fibo = "START  pythonw C:\\Users\\shengmei\\Desktop\\Flow\\Loops\\Fibo1.pyw"
            for i in range(1, cur_benchmark + 1):
                os.system(fibo)
    else:
        if cur == 4:
            cur_benchmark = 44
            os.system(
                f'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw {1} {1.0} {2.0}'
            )
        elif cur == 5:
            cur_benchmark = 55
            os.system(
                f'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw {1} {0.25} {0.5}'
            )
        else:
            cur_benchmark = 66
            os.system(
                f'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw {2} {4.0} {6.0}'
            )
        # cmd = "START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw"
        # os.system(cmd)
    ## if we need to randomize
    # condition = random.randint(1, 3)  #contant condition or variations
    # cur_benchmark = 0
    # if condition < 3: #constant condition
    #     cur_benchmark = random.randint(min_benchmark, max_benchmark)
    #     #run benchmarks
    #
    #     #fibo = "C:/Users/shengmei/Desktop/Flow/Loops/loop1.bat"
    #     fibo = "START "" pythonw C:\\Users\\shengmei\\Desktop\\Flow\\Loops\\Fibo1.pyw"
    #     for i in range(1, cur_benchmark + 1):
    #         os.system(fibo)
    # else:
    #     cmd = "START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw"
    #     os.system(cmd)

    # call API to play game
    log.write(
        datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        + " "
        + str(cur_benchmark)
        + " benchmarks\n"
    )
    log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " game started\n")
    log.write(
        datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        + " Round "
        + str(count)
        + " \n"
    )
    set_focus()

    # mouse and keyboard
    cmd = 'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\keyboard.pyw'
    os.system(cmd)

    cmd = 'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\mouse.pyw'
    os.system(cmd)

    # presentMon
    cmd = 'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\PresentMon.pyw'
    os.system(cmd)

    # game playing
    time.sleep(60)

    # game ending, kill benchmarks
    # os.system("taskkill /f /im cmd.exe")
    os.system("taskkill /f /im pythonw.exe")
    # os.system("wmic process where \"name=\'PresentMon64-dev210107.exe\'\" delete")

    # log performance
    shutil.copy2(
        scorePath,
        f"C:\\Users\\shengmei\\Documents\\Score\\score{count}_{cur_benchmark}.log",
    )
    # myScreenshot = pyautogui.screenshot()
    # myScreenshot.save(f'C:\\Users\\shengmei\\Documents\\Screenshots\\valorant_{count}_{cur_benchmark}.png')
    log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " game ended\n")

    # log mouse and keyboard
    shutil.move(
        "C:\\Users\\shengmei\\Documents\\mouse_log.txt",
        f"C:\\Users\\shengmei\\Documents\\Evlog\\mouse_{count}_{cur_benchmark}.txt",
    )
    shutil.move(
        "C:\\Users\\shengmei\\Documents\\keyboard_log.txt",
        f"C:\\Users\\shengmei\\Documents\\Evlog\\keyboard_{count}_{cur_benchmark}.txt",
    )

    # PresentMon
    time.sleep(2)
    os.system("taskkill /f /im PresentMon64-dev210107.exe")
    shutil.move(
        "C:\\Users\\shengmei\\Documents\\PresentMon.csv",
        f"C:\\Users\\shengmei\\Documents\\PresentMon\\PresentMon_{count}_{cur_benchmark}.csv",
    )

    # call API for QoE
    cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\QoE\\QoE.py"
    os.system(cmd)
    log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " survey taken\n")

    # Store the data from this round (we only need to move QoE data)
    if os.path.exists("C:/Users/shengmei/Documents/QoE.txt"):
        shutil.move(
            "C:/Users/shengmei/Documents/QoE.txt",
            f"C:/Users/shengmei/Documents/QoEs/QoE_{count}_{cur_benchmark}.txt",
        )

    if os.path.exists("C:/Users/shengmei/Documents/chaos.txt"):
        shutil.move(
            "C:/Users/shengmei/Documents/chaos.txt",
            f"C:/Users/shengmei/Documents/Chaos/chaos_{count}_{cur_benchmark}.txt",
        )

    # Next round
    cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\Next\\next.py"
    os.system(cmd)
    count = count + 1
    ind = ind + 1
    if count == 14:
        if fr2 == 60:
            kill_RTSS()
        else:
            kill_RTSS120()
# terminate valorant and remove performance log
os.system("taskkill /f /im VALORANT-Win64-Shipping.exe")
time.sleep(2)
# os.system("taskkill /f /im VALORANT.exe")
shutil.move(scorePath, f"C:\\Users\\shengmei\\Documents\\Score\\score_all.log")
log.close()

# zip files (may change later)
# filename = datetime.now().strftime("T-%d-%b-%Y-(%H-%M-%S-%f)")
path = f"C:\\Users\\shengmei\\Documents\\Valorant"
os.makedirs(path)
shutil.move("C:\\Users\\shengmei\\Documents\\QoEs", path)
shutil.move("C:\\Users\\shengmei\\Documents\\Score", path)
shutil.move("C:\\Users\\shengmei\\Documents\\Evlog", path)
shutil.move("C:\\Users\\shengmei\\Documents\\PresentMon", path)
shutil.move("C:\\Users\\shengmei\\Documents\\Chaos", path)
shutil.move("C:/Users/shengmei/Documents/scriptLogVa.txt", path)
# shutil.move("C:\\Users\\shengmei\\Documents\\Screenshots", path)

# shutil.make_archive(filename, 'zip', path)
# log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " data archived")
# log.close()

# #Testing end window
# cmd = 'python C:\\Users\\shengmei\\Desktop\\Flow\\Thanks\\thanks.py'
# os.system(cmd)
