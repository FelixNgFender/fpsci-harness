import contextlib
import pathlib
from collections.abc import Iterator

from harness import constants, process
from harness.monitoring import keyboard, mouse


@contextlib.contextmanager
def latency_context(results_dir: pathlib.Path, latency_ms: int | None) -> Iterator[None]:
    if latency_ms is None:
        yield
        return

    kb_thread = keyboard.start(results_dir / constants.KEYBOARD_LOG)
    mouse_thread = mouse.start(results_dir / constants.MOUSE_LOG)
    nvlatency_process = None
    if latency_ms != 0:
        nvlatency_process = process.start_nvlatency(
            latency_ms,
            results_dir / constants.NVLATECY_STDOUT,
            results_dir / constants.NVLATENCY_STDERR,
        )

    try:
        yield
    finally:
        if nvlatency_process:
            nvlatency_process.kill()
        kb_thread.stop()
        mouse_thread.stop()
