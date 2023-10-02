import datetime
import win32api
from random import randrange as rndrg
import winreg
import sys
import json
import os

HELP_TEXT = [
    "Программа для установки нужной даты со случайным временем!\n",
    "\n",
    'Введите "help" или "h" в любом регистре для получения помощи.\n',
    "Пример:\n",
    " - python {name} help\n",
    "\n",
    'Запустите приложение по шаблону "python {name} arg arg arg" в',
    " аргументах задайте дату в порядке DD MM YYYY\n",
    "Пример:\n",
    " - python {name} 25 9 2023 - установит 25 сентября 2023 года\n",
    " - python {name} 25 9 - установит 25 сентября текущего года\n",
    " - python {name} 25 - установит 25 число текучего месяца и года\n",
    "\n",
    "Для включения синхронизации времени с сервером",
    ' NTP введите "clear" или "c"\n',
    "Пример:\n",
    " - python {name} clear\n",
    "\n",
    "Запуск без параметров позволит взять данные для",
    ' даты из файла "date.json"\n',
    "Пример:\n",
    " - python {name}\n",
]


class RegEdit:
    @classmethod
    def _create_key(cls, head, tail) -> winreg.HKEYType:
        return winreg.OpenKey(
            head,
            tail,
            0,
            winreg.KEY_ALL_ACCESS,
        )

    @classmethod
    def disable_ubdate_time(cls):
        key = cls._create_key(
            winreg.HKEY_LOCAL_MACHINE,
            "SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters",
        )
        print("disable_ubdate_time")
        winreg.SetValueEx(key, "Type", None, winreg.REG_SZ, "NoSync")
        winreg.CloseKey(key)

    @classmethod
    def enable_ubdate_time(cls):
        key = cls._create_key(
            winreg.HKEY_LOCAL_MACHINE,
            "SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters",
        )
        print("enable_ubdate_time")
        winreg.SetValueEx(key, "Type", None, winreg.REG_SZ, "NTP")
        winreg.CloseKey(key)


def get_random_time():
    return (rndrg(0, 22), rndrg(0, 59), rndrg(0, 59), rndrg(0, 999))


def win_set_time(date_tuple, time_tuple):
    RegEdit.disable_ubdate_time()
    try:
        day_of_week = datetime.datetime(*date_tuple).isocalendar()[2]
    except Exception as error:
        print(error)
        sys.exit()
    try:
        new_date = (
            date_tuple[:2] + (day_of_week,) + (date_tuple[2],) + time_tuple
        )
    except Exception as error:
        print(error)
        sys.exit()
    win32api.SetSystemTime(*new_date)


def help_argument():
    print("".join(HELP_TEXT).format(name=os.path.basename(__file__)))
    sys.exit()


def clear_date():
    RegEdit.enable_ubdate_time()
    os.system("w32tm /resync")
    sys.exit()


def get_date_today() -> tuple[int, int, int]:
    today = datetime.datetime.now()
    return today.year, today.month, today.day


def get_date_from_arguments(arguments: list[str]):
    data: dict = {}
    if len(arguments) >= 1:
        data["day"] = arguments[0]
    if len(arguments) >= 2:
        data["month"] = arguments[1]
    if len(arguments) >= 3:
        data["year"] = arguments[2]
    year, month, day = get_date_today()
    try:
        year = int(data.get("year", year))
        month = int(data.get("month", month))
        day = int(data.get("day", day))
    except Exception as error:
        print(error)
    return year, month, day


def get_date_from_file() -> tuple:
    try:
        with open("date.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as error:
        print(error)
        sys.exit()
    year, month, day = get_date_today()
    try:
        year = int(data.get("year", year))
        month = int(data.get("month", month))
        day = int(data.get("day", day))
    except Exception as error:
        print(error)
    return year, month, day


def check_arguments():
    arguments = sys.argv[1:]
    if len(arguments) == 0:
        return get_date_from_file()
    if arguments[0].lower() in ("help" or "h"):
        help_argument()
    if arguments[0].lower() in ("clear" or "c"):
        clear_date()
    return get_date_from_arguments(arguments)


if __name__ == "__main__":
    date_tuple = check_arguments()
    time_tuple = get_random_time()
    win_set_time(date_tuple, time_tuple)
