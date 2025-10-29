import random
import time
import pyautogui
import os
from datetime import datetime
import shutil
from pywinauto.application import Application
import subprocess
from os import startfile

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
    # app = Application().connect(title='Rocket League (64-bit, DX11, Cooked)')
    # app['Rocket League (64-bit, DX11, Cooked)'].set_focus()
    pyautogui.click(x=610, y=1052, clicks=1, interval=0, button="left")


def pause():
    pyautogui.keyDown("esc")
    time.sleep(1)
    pyautogui.click(x=957, y=558, clicks=1, interval=0, button="left")  # pause


def unpause():
    time.sleep(1)
    pyautogui.click(x=957, y=558, clicks=1, interval=0, button="left")  # pause
    time.sleep(1)
    pyautogui.click(x=960, y=410, clicks=1, interval=0, button="left")  # unpause
    # pyautogui.keyDown('esc')


def start_rocket():
    pyautogui.FAILSAFE = False
    pyautogui.doubleClick(x=35, y=525)
    time.sleep(3)
    # pyautogui.click(x=660, y=1418, clicks=1, interval=0, button='left')  # set focus
    pyautogui.click(x=610, y=1060, clicks=1, interval=0, button="left")
    time.sleep(22)
    pyautogui.click(
        x=35, y=525, clicks=1, interval=0, button="left"
    )  # click any button
    time.sleep(1.5)
    # pyautogui.click(x=247, y=657, clicks=1, interval=0, button='left')  # play
    pyautogui.click(x=187, y=500, clicks=1, interval=0, button="left")  # play
    time.sleep(1.5)
    # pyautogui.click(x=1710, y=970, clicks=1, interval=0, button='left')  # play
    pyautogui.click(x=1285, y=728, clicks=1, interval=0, button="left")
    time.sleep(1.5)
    # pyautogui.click(x=1568, y=736, clicks=2, interval=1.5, button='left')  # play
    pyautogui.click(x=1169, y=547, clicks=2, interval=1.5, button="left")
    time.sleep(1.5)
    # pyautogui.click(x=710, y=1060, clicks=1, interval=0, button='left')  # play
    pyautogui.click(x=1169, y=547, clicks=2, interval=1.5, button="left")
    time.sleep(1.5)
    # pyautogui.click(x=1127, y=865, clicks=1, interval=0, button='left')  # play
    pyautogui.click(x=525, y=796, clicks=1, interval=0, button="left")
    time.sleep(1.5)
    # pyautogui.click(x=435, y=350, clicks=1, interval=0, button='left')  # play
    pyautogui.click(x=844, y=649, clicks=1, interval=0, button="left")
    time.sleep(1.5)
    pyautogui.click(x=333, y=271, clicks=1, interval=0, button="left")


def kill_RTSS120():
    os.system("wmic process where \"name='RTSS120.exe'\" delete")
    os.system("wmic process where \"name='EncoderServer.exe'\" delete")
    os.system("wmic process where \"name='RTSSHooksLoader64.exe'\" delete")


def kill_RTSS():
    os.system("wmic process where \"name='RTSS.exe'\" delete")
    os.system("wmic process where \"name='EncoderServer.exe'\" delete")
    os.system("wmic process where \"name='RTSSHooksLoader64.exe'\" delete")


cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\rocket\\valorant.py"
os.system(cmd)

startfile("C:\\Users\\shengmei\\Desktop\\Flow\\Rocket.mp4")
while process_exists("Video.UI.exe"):
    time.sleep(2)


# start strange Brigade
start_rocket()
set_focus()
time.sleep(2)
pause()

min_benchmark = 0
max_benchmark = 10

count = 0

# create folders for screenshots (performance) and QoE

QoEs = "C:\\Users\\shengmei\\Documents\\QoEs"
if not os.path.exists(QoEs):
    os.makedirs(QoEs)

Evlog = "C:\\Users\\shengmei\\Documents\\Evlog"
if not os.path.exists(Evlog):
    os.makedirs(Evlog)

PresentMon = "C:\\Users\\shengmei\\Documents\\PresentMon"
if not os.path.exists(PresentMon):
    os.makedirs(PresentMon)

Screenshots = "C:\\Users\\shengmei\\Documents\\Screenshots"
if not os.path.exists(Screenshots):
    os.makedirs(Screenshots)

Chaos = "C:\\Users\\shengmei\\Documents\\Chaos"
if not os.path.exists(Chaos):
    os.makedirs(Chaos)


##Needs screenshot for this game
# scorePath = "C:\\Users\\shengmei\\AppData\\Local\VALORANT\\Saved\\Logs\\ShooterGame.log"


# Name of the next game

# scriptLog
log = open("C:/Users/shengmei/Documents/scriptLogRl.txt", "a")

log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " : Rocket time\n")
log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " : Test round\n")

# Test round first
# call API to play game
cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\Test\\test.py"
os.system(cmd)
set_focus()
time.sleep(1)
unpause()

# playing
time.sleep(60)
myScreenshot = pyautogui.screenshot()
myScreenshot.save(f"C:\\Users\\shengmei\\Documents\\Screenshots\\valorant_Test.png")

# cmd = 'python C:\\Users\\shengmei\\Desktop\\Flow\\Testend\\testend.py'
# os.system(cmd)
log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " : Test round ended\n")
pause()

cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\NextRL\\next.py"
os.system(cmd)

# No QoE for test round
# Test round ended API
REPEAT = [0, 14, 17, 20]
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
            time.sleep(2)
        else:
            os.system(
                'START "" "C:\\Program Files (x86)\\RivaTuner Statistics Server 120\\RTSS120.exe"'
            )
            time.sleep(2)
        log.write(
            datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            + " "
            + str(fr1)
            + " fr "
            + str(fr2)
            + " fr\n"
        )

    if count == 7:  # next
        ind = 0
        if fr2 == 60:
            kill_RTSS120()
            time.sleep(5)
            os.system(
                'START "" "C:\\Program Files (x86)\\RivaTuner Statistics Server\\RTSS.exe"'
            )
            time.sleep(7)
        else:
            kill_RTSS()
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
                f'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw {3} {1.0} {2.0}'
            )
        elif cur == 5:
            cur_benchmark = 55
            os.system(
                f'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw {3} {0.25} {0.5}'
            )
        else:
            cur_benchmark = 66
            os.system(
                f'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw {4} {4.0} {6.0}'
            )
    # while count < 15:
    #     condition = random.randint(1, 2)  #contant condition or variations
    #     cur_benchmark = 0
    #     if condition < 3: #constant condition
    #         cur_benchmark = random.randint(min_benchmark, max_benchmark)
    #         #run benchmarks
    #         fibo = "START "" pythonw C:\\Users\\shengmei\\Desktop\\Flow\\Loops\\Fibo1.pyw"
    #         #fibo = "C:/Users/shengmei/Desktop/Flow/Loops/loop1.bat"
    #         for i in range(1, cur_benchmark + 1):
    #             os.system(fibo)
    #     else:
    #         cmd = "START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflowRL.pyw"
    #         os.system(cmd)
    #

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
    time.sleep(1)
    unpause()

    # mouse and keyboard
    cmd = 'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\keyboard.pyw'
    os.system(cmd)

    cmd = 'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\mouse.pyw'
    os.system(cmd)

    # presentMon
    cmd = (
        'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\PresentMonRL.pyw'
    )
    os.system(cmd)

    # game playing, and take screenshots at the end

    time.sleep(60)

    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(
        f"C:\\Users\\shengmei\\Documents\\Screenshots\\rocket_{count}_{cur_benchmark}.png"
    )

    # game ending, kill benchmarks
    # os.system("taskkill /f /im cmd.exe")
    os.system("taskkill /f /im pythonw.exe")
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

    # Pause the game
    time.sleep(1)
    pause()

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
    cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\NextRL\\next.py"
    os.system(cmd)
    count = count + 1
    ind = ind + 1
    if count == 14:
        if fr2 == 60:
            kill_RTSS()
        else:
            kill_RTSS120()
        time.sleep(2)
# terminate valorant and remove performance log
os.system("taskkill /f /im RocketLeague.exe")
# os.system("taskkill /f /im VALORANT.exe")
# shutil.move(scorePath, f'C:\\Users\\shengmei\\Documents\\Score\\score_all.log')
log.close()

# zip files (may change later)
# filename = datetime.now().strftime("T-%d-%b-%Y-(%H-%M-%S-%f)")
path = "C:\\Users\\shengmei\\Documents\\Rocket"
os.makedirs(path)
shutil.move("C:\\Users\\shengmei\\Documents\\QoEs", path)
shutil.move("C:\\Users\\shengmei\\Documents\\Screenshots", path)
shutil.move("C:\\Users\\shengmei\\Documents\\Evlog", path)
shutil.move("C:\\Users\\shengmei\\Documents\\PresentMon", path)
shutil.move("C:/Users/shengmei/Documents/scriptLogRl.txt", path)
shutil.move("C:\\Users\\shengmei\\Documents\\Chaos", path)

# shutil.move("C:\\Users\\shengmei\\Documents\\Screenshots", path)

# shutil.make_archive(filename, 'zip', path)
# log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " data archived")


# Testing end window
# cmd = 'python C:\\Users\\shengmei\\Desktop\\Flow\\Thanks\\thanks.py'
# os.system(cmd)
