"""
Every parameter (except for CONFIG_FILE) can be
overwritten by external config file
"""
import mailcap
import os
import platform
import runpy
from typing import Any, Dict, List, Optional, Tuple

_os_name = platform.system()
_linux = "Linux"
_global_mailcap = mailcap.getcaps()


CONFIG_DIR: str = os.path.expanduser("~/.config/arigram/")
CONFIG_FILE: str = os.path.join(CONFIG_DIR, "config.py")
FILES_DIR: str = os.path.expanduser("~/.cache/arigram/")
DRAFTS_FILE: str = os.path.join(FILES_DIR, "drafts.json")
MAILCAP_FILE: Optional[str] = None

LOG_LEVEL: str = "INFO"
LOG_PATH: str = os.path.expanduser("~/.local/share/arigram/")

API_ID: str = "559815"
API_HASH: str = "fd121358f59d764c57c55871aa0807ca"

PHONE: Optional[str] = None
ENC_KEY: str = ""

TDLIB_PATH: Optional[str] = None
TDLIB_VERBOSITY: int = 0

MAX_DOWNLOAD_SIZE: str = "10MB"

NOTIFY_FUNCTION: Optional[Any] = None

VIEW_TEXT_CMD: str = "less"

# for more info see https://trac.ffmpeg.org/wiki/Capture/ALSA
VOICE_RECORD_CMD: str = (
    "ffmpeg -f alsa -i hw:0 -c:a libopus -b:a 32k {file_path}"
    if _os_name == _linux
    else "ffmpeg -f avfoundation -i ':0' -c:a libopus -b:a 32k {file_path}"
)

EDITOR: str = os.environ.get("EDITOR", "vim")
_, __MAILCAP_EDITOR = mailcap.findmatch(_global_mailcap, "text/markdown")

if __MAILCAP_EDITOR:
    EDITOR = str(__MAILCAP_EDITOR["view"]).split(" ", 1)[0]

LONG_MSG_CMD: str = f"{EDITOR} '{{file_path}}'"

DEFAULT_OPEN: str = (
    "xdg-open {file_path}" if _os_name == _linux else "open {file_path}"
)

CHAT_FLAGS: Dict[str, str] = {}

MSG_FLAGS: Dict[str, str] = {}

ICON_PATH: str = os.path.join(
    os.path.dirname(__file__), "resources", "arigram.png"
)

URL_VIEW: Optional[str] = None

USERS_COLOURS: Tuple[int, ...] = tuple(range(2, 16))

KEEP_MEDIA: int = 7

FILE_PICKER_CMD: Optional[str] = None

DOWNLOAD_DIR: str = os.path.expanduser("~/Downloads/")

EXTRA_FILE_CHOOSER_PATHS: List[str] = ["..", "/", "~"]

CUSTOM_KEYBINDS: Dict[str, Dict[str, Any]] = {}

TRUNCATE_LIMIT: int = 15

EXTRA_TDLIB_HEADEARS: Dict[Any, Any] = {}

if os.path.isfile(CONFIG_FILE):
    config_params = runpy.run_path(CONFIG_FILE)  # type: ignore
    for param, value in config_params.items():
        if param.isupper():
            globals()[param] = value
else:
    os.makedirs(CONFIG_DIR, exist_ok=True)

    if not PHONE:
        print(
            "Enter your phone number in international format, including country code (example: +5037754762346)"
        )
        PHONE = input("(phone) ")
        if not PHONE.startswith("+"):
            PHONE = "+" + PHONE

    with open(CONFIG_FILE, "a") as f:
        f.write(f'\nPHONE = "{PHONE}"\n')
