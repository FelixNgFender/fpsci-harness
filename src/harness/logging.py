import os
import logging


def configure_log_to_file(logger: logging.Logger, filename: str | os.PathLike) -> None:
    logger.setLevel(logging.DEBUG)

    # Create a file handler for this module only
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.DEBUG)

    # Define formatter
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d,%(levelname)s,%(message)s", "%Y-%m-%d:%H:%M:%S"
    )
    file_handler.setFormatter(formatter)

    # Attach handler only to this logger
    logger.addHandler(file_handler)

    # Avoid propagating messages to root logger
    logger.propagate = False
