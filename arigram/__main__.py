import logging.handlers
import signal
import sys
import threading
from curses import window, wrapper  # type: ignore
from functools import partial
from types import FrameType

import arigram
from arigram import config, update_handlers, utils
from arigram.controllers import Controller
from arigram.models import Model
from arigram.tdlib import Tdlib
from arigram.views import ChatView, MsgView, StatusView, View

log = logging.getLogger(__name__)


def run(tg: Tdlib, stdscr: window) -> None:

    # handle ctrl+c, to avoid interrupting arigram when subprocess is called
    def interrupt_signal_handler(sig: int, frame: FrameType) -> None:
        # TODO: draw on status pane: to quite press <q>
        del sig, frame
        log.info("Interrupt signal is handled and ignored on purpose.")

    signal.signal(signal.SIGINT, interrupt_signal_handler)  # type: ignore

    model = Model(tg)
    status_view = StatusView(stdscr)
    msg_view = MsgView(stdscr, model)
    chat_view = ChatView(stdscr, model)
    view = View(stdscr, chat_view, msg_view, status_view)
    controller = Controller(model, view, tg)

    # hanlde resize of terminal correctly
    signal.signal(signal.SIGWINCH, controller.resize_handler)

    for msg_type, handler in update_handlers.handlers.items():
        tg.add_update_handler(msg_type, partial(handler, controller))

    thread = threading.Thread(target=controller.run)
    thread.setDaemon(True)
    thread.start()

    controller.load_custom_keybindings()
    controller.draw()


def parse_args() -> None:
    """Parse CLI arguments"""

    if len(sys.argv) < 2:
        return

    if sys.argv[1] in ("-v", "--version"):
        print("Terminal Telegram client")
        print("Version:", arigram.__version__)
        sys.exit()


def main() -> None:
    """Main function"""

    parse_args()

    utils.cleanup_cache()

    tg = Tdlib(
        config.EXTRA_TDLIB_HEADEARS,
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        phone=config.PHONE,
        database_encryption_key=config.ENC_KEY,
        files_directory=config.FILES_DIR,
        tdlib_verbosity=config.TDLIB_VERBOSITY,
        library_path=config.TDLIB_PATH,
    )
    tg.login()

    utils.setup_log()
    utils.set_shorter_esc_delay()

    wrapper(partial(run, tg))


if __name__ == "__main__":
    main()
