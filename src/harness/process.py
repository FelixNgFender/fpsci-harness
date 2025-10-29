import os
import subprocess
import harness.constants as constants


def kill_nvlatency() -> None:
    # os.system("wmic process where \"name='RTSS.exe'\" delete")
    pass


def process_exists(name: str) -> bool:
    """Returns whether the process with the specified name exists"""
    call = "TASKLIST", "/FI", "imagename eq %s" % name
    # use built-in check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split("\r\n")[-1]
    # because Fail message could be translated and is cropped at 25 chars
    return last_line.lower()[:25].startswith(name.lower()[:25])


def kill_process_name(name: str) -> None:
    os.system(f"taskkill /f /im {name}")


def kill_process(p: subprocess.Popen) -> None:
    subprocess.check_call(["taskkill", "/F", "/T", "/PID", str(p.pid)])


def start_process(url: str) -> subprocess.Popen:
    print(url)
    return subprocess.Popen(f"start {url}", shell=True)


def is_media_player_alive() -> bool:
    return process_exists(constants.MEDIA_PLAYER_PROCESS_NAME)


def play_valorant_tutorial() -> None:
    os.startfile(constants.FITTS_TUTORIAL_PATH)
