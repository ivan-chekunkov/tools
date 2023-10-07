import json
import logging
import shutil
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

COUNT_FILES = 0
ERRORS = 0


class NotDriveName(Exception):
    pass


def create_path(path: Path) -> bool:
    if not path.parent.exists():
        if not path.parents[-1].exists():
            raise NotDriveName
        path.parent.mkdir(parents=True)
        return True


def copy_file(old_path: Path, new_path: Path) -> None:
    global COUNT_FILES
    global ERRORS
    if new_path.is_dir() and new_path.exists():
        return
    create_path(Path(new_path))
    try:
        shutil.copy(old_path, new_path)
        COUNT_FILES += 1
        success_log.info("File {} copy in {}".format(old_path, new_path))
    except Exception as error:
        ERRORS += 1
        error_log.error(error)


def view_path(root: Path, path: Path, out_root: Path, step=""):
    files_and_dirs = root.joinpath(path).iterdir()
    if not files_and_dirs:
        copy_file(root.joinpath(path), out_root.joinpath(path))
    for name in files_and_dirs:
        if name.is_dir():
            view_path(root, name, out_root, step=step + "--")
        new_path = out_root.joinpath(
            str(name).replace(str(root).rstrip("\\") + "\\", "")
        )
        copy_file(root.joinpath(name), new_path)
        main_log.info("{}{} {}".format(step, "|", new_path))


def get_root_and_path(data: list[str]) -> tuple[Path, Path]:
    for elem in map(Path, data):
        yield elem.parent, elem.name


def start():
    with open("./path_backup.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for root, path in get_root_and_path(data["path_in"]):
        view_path(root, path, Path(data["path_out"]), step="--")


if __name__ == "__main__":
    start()
    main_log.info("Количество файлов -> {}".format(COUNT_FILES))
    main_log.info("Ошибочных файлов -> {}".format(ERRORS))
