import os
import sys
import logging
import platform

logger = logging.getLogger(__name__)

class StartupManager:
    """
    Cross-platform manager for handling 'Run on System Startup' preferences.
    Supports Windows (Registry), macOS (LaunchAgents), and Linux (XDG Autostart).
    """
    def __init__(self, app_name: str = "SpotHashWidget"):
        self.app_name = app_name
        self.os_type = platform.system().lower()

    def get_startup_command(self) -> str:
        """
        Returns the complete startup command string:
        sys.executable for frozen builds, or safely quoted sys.executable + script path for source builds.
        """
        if getattr(sys, 'frozen', False):
            return f'"{sys.executable}"'
        else:
            return f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'

    def get_program_arguments(self) -> list[str]:
        """
        Returns program arguments list for macOS plist.
        """
        if getattr(sys, 'frozen', False):
            return [sys.executable]
        else:
            return [sys.executable, os.path.abspath(sys.argv[0])]

    def is_startup_enabled(self) -> bool:
        """Checks if the application is currently registered for system startup."""
        try:
            if "windows" in self.os_type:
                return self._check_windows_registry()
            elif "darwin" in self.os_type:
                return self._check_macos_plist()
            elif "linux" in self.os_type:
                return self._check_linux_desktop()
        except Exception as e:
            logger.error("Error checking startup status: %s", e)
        return False

    def set_startup(self, enable: bool) -> bool:
        """Enables or disables system startup registration."""
        try:
            if "windows" in self.os_type:
                return self._set_windows_registry(enable)
            elif "darwin" in self.os_type:
                return self._set_macos_plist(enable)
            elif "linux" in self.os_type:
                return self._set_linux_desktop(enable)
        except Exception as e:
            logger.error("Failed to update startup status (enable=%s): %s", enable, e)
        return False

    # --- Windows Implementation ---
    def _check_windows_registry(self) -> bool:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ) as key:
                val, _ = winreg.QueryValueEx(key, self.app_name)
                expected = self.get_startup_command()
                return val.strip().lower() == expected.strip().lower()
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.debug("Windows registry check error: %s", e)
            return False

    def _set_windows_registry(self, enable: bool) -> bool:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        cmd = self.get_startup_command()
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                if enable:
                    winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, cmd)
                    logger.info("Added to Windows Registry startup: %s", cmd)
                else:
                    try:
                        winreg.DeleteValue(key, self.app_name)
                        logger.info("Removed from Windows Registry startup.")
                    except FileNotFoundError:
                        pass
            return True
        except Exception as e:
            logger.error("Windows registry modification error: %s", e)
            return False

    # --- macOS Implementation ---
    def _check_macos_plist(self) -> bool:
        plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{self.app_name}.plist")
        if not os.path.exists(plist_path):
            return False
        try:
            import plistlib
            with open(plist_path, "rb") as f:
                data = plistlib.load(f)
                return data.get("ProgramArguments") == self.get_program_arguments()
        except Exception as e:
            logger.debug("macOS plist check error: %s", e)
            return False

    def _set_macos_plist(self, enable: bool) -> bool:
        import plistlib
        plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{self.app_name}.plist")
        os.makedirs(os.path.dirname(plist_path), exist_ok=True)
        
        if enable:
            plist_data = {
                "Label": self.app_name,
                "ProgramArguments": self.get_program_arguments(),
                "RunAtLoad": True,
                "KeepAlive": False
            }
            try:
                with open(plist_path, "wb") as f:
                    plistlib.dump(plist_data, f)
                logger.info("Created macOS LaunchAgent at %s", plist_path)
                return True
            except Exception as e:
                logger.error("Failed to create macOS plist: %s", e)
                return False
        else:
            try:
                if os.path.exists(plist_path):
                    os.remove(plist_path)
                    logger.info("Removed macOS LaunchAgent.")
                return True
            except Exception as e:
                logger.error("Failed to remove macOS plist: %s", e)
                return False

    # --- Linux Implementation ---
    def _check_linux_desktop(self) -> bool:
        desktop_path = os.path.expanduser(f"~/.config/autostart/{self.app_name}.desktop")
        if not os.path.exists(desktop_path):
            return False
        try:
            with open(desktop_path, "r", encoding="utf-8") as f:
                content = f.read()
                expected_exec = f"Exec={self.get_startup_command()}"
                return expected_exec in content
        except Exception as e:
            logger.debug("Linux desktop check error: %s", e)
            return False

    def _set_linux_desktop(self, enable: bool) -> bool:
        autostart_dir = os.path.expanduser("~/.config/autostart")
        desktop_path = os.path.join(autostart_dir, f"{self.app_name}.desktop")
        
        if enable:
            os.makedirs(autostart_dir, exist_ok=True)
            desktop_content = f"""[Desktop Entry]
Type=Application
Name={self.app_name}
Exec={self.get_startup_command()}
X-GNOME-Autostart-enabled=true
"""
            try:
                with open(desktop_path, "w", encoding="utf-8") as f:
                    f.write(desktop_content)
                logger.info("Created Linux autostart desktop entry at %s", desktop_path)
                return True
            except Exception as e:
                logger.error("Failed to create Linux desktop file: %s", e)
                return False
        else:
            try:
                if os.path.exists(desktop_path):
                    os.remove(desktop_path)
                    logger.info("Removed Linux autostart desktop entry.")
                return True
            except Exception as e:
                logger.error("Failed to remove Linux desktop file: %s", e)
                return False
