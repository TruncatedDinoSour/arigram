"""
Every parameter (except for CONFIG_FILE) can be
overwritten by external config file
"""
import mailcap
import os
import platform
import runpy
from typing import Any, Dict, Optional

_os_name = platform.system()
_linux = "Linux"
_global_mailcap = mailcap.getcaps()


CONFIG_DIR = os.path.expanduser("~/.config/arigram/")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.py")
FILES_DIR = os.path.expanduser("~/.cache/arigram/")
DRAFTS_FILE = os.path.join(FILES_DIR, "drafts.json")
MAILCAP_FILE: Optional[str] = None

LOG_LEVEL = "INFO"
LOG_PATH = os.path.expanduser("~/.local/share/arigram/")

API_ID = "559815"
API_HASH = "fd121358f59d764c57c55871aa0807ca"

PHONE = None
ENC_KEY = ""

TDLIB_PATH = None
TDLIB_VERBOSITY = 0

MAX_DOWNLOAD_SIZE = "10MB"

NOTIFY_FUNCTION = None

VIEW_TEXT_CMD = "less"
FZF = "fzf"

if _os_name == _linux:
    # for more info see https://trac.ffmpeg.org/wiki/Capture/ALSA
    VOICE_RECORD_CMD = (
        "ffmpeg -f alsa -i hw:0 -c:a libopus -b:a 32k {file_path}"
    )
else:
    VOICE_RECORD_CMD = (
        "ffmpeg -f avfoundation -i ':0' -c:a libopus -b:a 32k {file_path}"
    )


EDITOR = os.environ.get("EDITOR", "vim")
_, __MAILCAP_EDITOR = mailcap.findmatch(_global_mailcap, "text/markdown")

if __MAILCAP_EDITOR:
    EDITOR = str(__MAILCAP_EDITOR["view"]).split(" ", 1)[0]

LONG_MSG_CMD = f"{EDITOR} '{{file_path}}'"

if _os_name == _linux:
    DEFAULT_OPEN = "xdg-open {file_path}"
else:
    DEFAULT_OPEN = "open {file_path}"

if _os_name == _linux:
    if os.environ.get("WAYLAND_DISPLAY"):
        COPY_CMD = "wl-copy"
    else:
        COPY_CMD = "xclip -selection cliboard"
else:
    COPY_CMD = "pbcopy"

CHAT_FLAGS: Dict[str, str] = {}

MSG_FLAGS: Dict[str, str] = {}

ICON_PATH = os.path.join(os.path.dirname(__file__), "resources", "arigram.png")

URL_VIEW = None

USERS_COLORS = tuple(range(2, 16))

KEEP_MEDIA = 7

FILE_PICKER_CMD = None

DOWNLOAD_DIR = os.path.expanduser("~/Downloads/")

EXTRA_FILE_CHOOSER_PATHS = ["..", "/", "~"]

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
