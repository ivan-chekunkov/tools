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


if __name__ == "__main__":
    pass
