import os
import pathlib
import subprocess


def process_exists(name: str) -> bool:
    """Return whether the process with the specified name exists."""
    call = "TASKLIST", "/FI", f"imagename eq {name}"
    # use built-in check_output right away
    output = subprocess.check_output(call).decode()  # noqa: S603
    # check in last line for process name
    last_line = output.strip().split("\r\n")[-1]
    # because Fail message could be translated and is cropped at 25 chars
    return last_line.lower()[:25].startswith(name.lower()[:25])


def kill_process_name(name: str) -> None:
    os.system(f"taskkill /f /im {name}")  # noqa: S605


def kill_process(p: subprocess.Popen) -> None:
    subprocess.check_call(["taskkill", "/F", "/T", "/PID", str(p.pid)])  # noqa: S603, S607


def start_process(url: str) -> subprocess.Popen:
    return subprocess.Popen(f"start {url}", shell=True)  # noqa: S602


def start_nvlatency(
    latency_ms: int,
    stdout_log_path: str | pathlib.Path,
    stderr_log_path: str | pathlib.Path,
) -> subprocess.Popen:
    stdout_log_path = pathlib.Path(stdout_log_path)
    stderr_log_path = pathlib.Path(stderr_log_path)
    return subprocess.Popen(  # noqa: S603
        ["input-injector.exe", "--latency", "constant", str(latency_ms)],  # noqa: S607
        stdout=pathlib.Path.open(stdout_log_path, "a"),
        stderr=pathlib.Path.open(stderr_log_path, "a"),
    )
