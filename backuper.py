import logging
from pathlib import Path


def get_logger(name: str, level: int) -> logging.Logger:
    logger = logging.getLogger(name)
    file_log = logging.FileHandler(
        "{}.log".format(name.capitalize()), encoding="UTF-8"
    )
    console_out = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger.setLevel(level)
    console_out.setFormatter(formatter)
    logger.addHandler(console_out)
    file_log.setFormatter(formatter)
    logger.addHandler(file_log)
    return logger


main_log = get_logger("main_logger", logging.INFO)
success_log = get_logger("success_logger", logging.INFO)
error_log = get_logger("error_logger", logging.ERROR)


class NotDriveName(Exception):
    pass


def create_path(path: Path) -> bool:
    if not path.parent.exists():
        if not path.parents[-1].exists():
            raise NotDriveName
        path.parent.mkdir(parents=True)
        return True
