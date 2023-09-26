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
    def _print_all_values_branch(cls, key):
        index = 0
        while True:
            try:
                print(winreg.EnumValue(key, index))
            except Exception:
                break
            index += 1

    @classmethod
    def disable_ubdate_time(cls):
        key = cls._create_key(
            winreg.HKEY_LOCAL_MACHINE,
            "SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters",
        )
        print("disable_ubdate_time")
        cls._print_all_values_branch(key)
        winreg.SetValueEx(key, "Type", None, winreg.REG_SZ, "NoSync")
        winreg.CloseKey(key)

    @classmethod
    def enable_numlock_on_start(cls):
        key = cls._create_key(
            winreg.HKEY_USERS,
            ".DEFAULT\\Control Panel\\Keyboard",
        )
        print("enable_numlock_on_start")
        cls._print_all_values_branch(key)
        winreg.SetValueEx(
            key, "InitialKeyboardIndicators", None, winreg.REG_SZ, "2147483650"
        )
        winreg.CloseKey(key)

    @classmethod
    def enable_shift_language_ctrlshift(cls):
        key = cls._create_key(
            winreg.HKEY_CURRENT_USER,
            "Keyboard Layout\\Toggle",
        )
        print("enable_shift_language_ctrlshift")
        cls._print_all_values_branch(key)
        winreg.SetValueEx(key, "Hotkey", None, winreg.REG_SZ, "2")
        winreg.SetValueEx(key, "Language Hotkey", None, winreg.REG_SZ, "2")
        winreg.SetValueEx(key, "Layout Hotkey", None, winreg.REG_SZ, "3")
        winreg.CloseKey(key)

    @classmethod
    def call_all(cls):
        cls.disable_ubdate_time()
        cls.enable_numlock_on_start()
        cls.enable_shift_language_ctrlshift()


RegEdit.call_all()
