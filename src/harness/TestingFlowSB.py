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
    # app = Application().connect(title_re='Strange Brigade')
    # app['Strange Brigade'].set_focus()
    pyautogui.click(x=610, y=1052, clicks=1, interval=0, button="left")


def start_sb():
    pyautogui.FAILSAFE = False
    pyautogui.doubleClick(x=185, y=45)  # double click
    time.sleep(2)
    pyautogui.doubleClick(x=825, y=457)  # middle page
    # pyautogui.doubleClick(x=1145, y=640) # middle page
    time.sleep(55)


def kill_RTSS120():
    os.system("wmic process where \"name='RTSS120.exe'\" delete")
    os.system("wmic process where \"name='EncoderServer.exe'\" delete")
    os.system("wmic process where \"name='RTSSHooksLoader64.exe'\" delete")


def kill_RTSS():
    os.system("wmic process where \"name='RTSS.exe'\" delete")
    os.system("wmic process where \"name='EncoderServer.exe'\" delete")
    os.system("wmic process where \"name='RTSSHooksLoader64.exe'\" delete")


# Name of the next game
cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\strange\\valorant.py"
os.system(cmd)

# play video and wait until close
startfile("C:\\Users\\shengmei\\Desktop\\Flow\\Strange.mp4")
while process_exists("Video.UI.exe"):
    time.sleep(2)

# start strange Brigade
start_sb()

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


# scriptLog
log = open("C:/Users/shengmei/Documents/scriptLogSb.txt", "a")

log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " : Strange time\n")
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
pyautogui.keyDown("esc")  # pause

cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\NextSB\\next.py"
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
            time.sleep(2)
        else:
            kill_RTSS()
            time.sleep(5)
            os.system(
                'START "" "C:\\Program Files (x86)\\RivaTuner Statistics Server 120\\RTSS120.exe"'
            )
            time.sleep(2)

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
    #         cmd = "START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\workflow.pyw"
    #         os.system(cmd)
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
    # mouse and keyboard
    cmd = 'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\keyboard.pyw'
    os.system(cmd)

    cmd = 'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\mouse.pyw'
    os.system(cmd)

    # presentMon
    cmd = (
        'START "" pythonw C:\\Users\\shengmei\\Documents\\TestingFlow\\PresentMonSB.pyw'
    )
    os.system(cmd)

    # game playing, take screenshots every 6 seconds

    ss = 0

    while ss < 10:
        time.sleep(6)
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(
            f"C:\\Users\\shengmei\\Documents\\Screenshots\\strange_{count}_{cur_benchmark}_{ss}.png"
        )
        ss = ss + 1

    # game playing
    # time.sleep(60)

    # game ending, kill benchmarks
    # os.system("taskkill /f /im cmd.exe")
    os.system("taskkill /f /im pythonw.exe")
    # log performance
    # shutil.copy2(scorePath, f'C:\\Users\\shengmei\\Documents\\Score\\score{count}_{cur_benchmark}.log')
    # myScreenshot = pyautogui.screenshot()
    # myScreenshot.save(f'C:\\Users\\shengmei\\Documents\\Strange\\Screenshots\\strange_{count}_{cur_benchmark}.png')
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
    pyautogui.keyDown("esc")

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
    cmd = "python C:\\Users\\shengmei\\Desktop\\Flow\\NextSB\\next.py"
    os.system(cmd)
    count = count + 1
    ind = ind + 1
    if count == 14:
        if fr2 == 60:
            kill_RTSS()
        else:
            kill_RTSS120()
# terminate valorant and remove performance log
os.system("taskkill /f /im StrangeBrigade_Vulkan.exe")
# os.system("taskkill /f /im VALORANT.exe")
# shutil.move(scorePath, f'C:\\Users\\shengmei\\Documents\\Score\\score_all.log')
log.close()

# zip files (may change later)
# filename = datetime.now().strftime("T-%d-%b-%Y-(%H-%M-%S-%f)")
path = "C:\\Users\\shengmei\\Documents\\Strange"
os.makedirs(path)
shutil.move("C:\\Users\\shengmei\\Documents\\QoEs", path)
shutil.move("C:\\Users\\shengmei\\Documents\\Screenshots", path)
shutil.move("C:\\Users\\shengmei\\Documents\\Evlog", path)
shutil.move("C:\\Users\\shengmei\\Documents\\PresentMon", path)
shutil.move("C:\\Users\\shengmei\\Documents\\Chaos", path)
shutil.move("C:/Users/shengmei/Documents/scriptLogSb.txt", path)

# shutil.move("C:\\Users\\shengmei\\Documents\\Screenshots", path)

# shutil.make_archive(filename, 'zip', path)
# log.write(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " data archived")


# Testing end window
# cmd = 'python C:\\Users\\shengmei\\Desktop\\Flow\\Thanks\\thanks.py'
# os.system(cmd)
