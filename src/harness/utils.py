import datetime

from harness import constants


def current_datetime_str() -> str:
    return datetime.datetime.now(tz=datetime.UTC).strftime(constants.DATEFMT_STR)
