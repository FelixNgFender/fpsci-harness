from datetime import datetime
from harness import constants


def current_datetime_str() -> str:
    return datetime.now().strftime(constants.DATEFMT_STR)
