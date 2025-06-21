#!/usr/bin/env python3
"""DisplayPi - simple kiosk launcher using Chromium.

This simple script opens a single URL in fullscreen (kiosk) mode using the
``chromium-browser`` application that comes with Raspberry Pi OS.
"""

import argparse
import subprocess
from typing import List



# URLs that can be displayed. ``flightradar`` is the default page while
# ``local`` can be used to show a locally hosted web application.
URLS = {
    "flightradar": "https://www.flightradar24.com/simple/",
    "local": "http://localhost:3000",
}

CHROMIUM_CMD = [
    "chromium-browser",
    "--noerrdialogs",
    "--kiosk",
]


def launch_chromium(urls: List[str]) -> subprocess.Popen:
    """Launch Chromium pointing to ``urls`` in kiosk mode."""
    cmd = CHROMIUM_CMD + urls
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch Chromium in kiosk mode")
    parser.add_argument(
        "--urls",
        nargs="+",
        choices=URLS.keys(),
        default=list(URLS.keys()),
        help="Pages to open as tabs",
    )
    args = parser.parse_args()

    from pynput import keyboard as kb

    urls = [URLS[name] for name in args.urls]
    proc = launch_chromium(urls)

    controller = kb.Controller()

    def on_press(key):
        if key == kb.Key.f5:
            controller.press(kb.Key.ctrl)
            controller.press(kb.Key.tab)
            controller.release(kb.Key.tab)
            controller.release(kb.Key.ctrl)
        elif key == kb.Key.f6:
            controller.press(kb.Key.ctrl)
            controller.press(kb.Key.shift)
            controller.press(kb.Key.tab)
            controller.release(kb.Key.tab)
            controller.release(kb.Key.shift)
            controller.release(kb.Key.ctrl)

    listener = kb.Listener(on_press=on_press)
    listener.start()

    try:
        proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate()
        proc.wait()
        listener.stop()
        listener.join()


if __name__ == "__main__":
    main()
