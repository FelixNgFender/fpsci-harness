import os
import pathlib
import subprocess


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
    return subprocess.Popen(f"start {url}", shell=True)


def kill_chrome() -> None:
    """WARNING: This will kill all Chrome instances"""
    subprocess.Popen("taskkill /F /IM chrome.exe", shell=True)


def start_nvlatency(
    latency_ms: int,
    stdout_log_path: str | pathlib.Path,
    stderr_log_path: str | pathlib.Path,
) -> subprocess.Popen:
    stdout_log_path = pathlib.Path(stdout_log_path)
    stderr_log_path = pathlib.Path(stderr_log_path)
    return subprocess.Popen(
        ["input-injector.exe", "--latency", "constant", str(latency_ms)],
        stdout=open(stdout_log_path, "a"),
        stderr=open(stderr_log_path, "a"),
    )


def kill_nvlatency() -> None:
    # os.system("wmic process where \"name='RTSS.exe'\" delete")
    pass
