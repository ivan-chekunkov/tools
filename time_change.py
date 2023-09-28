import datetime
import json
import sys
import winreg


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
