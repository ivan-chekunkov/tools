import datetime
import json
import sys
import winreg
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


if __name__ == "__main__":
    pass
