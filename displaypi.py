#!/usr/bin/env python3
"""DisplayPi - simple kiosk launcher using Chromium.

This simple script opens a single URL in fullscreen (kiosk) mode using the
``chromium-browser`` application that comes with Raspberry Pi OS.
"""

import argparse
import subprocess
import threading
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
    parser.add_argument(
        "--no-button",
        action="store_true",
        help="Do not show the control-tab overlay button",
    )
    args = parser.parse_args()

    from pynput import keyboard as kb
    from tkinter import Tk, Button

    urls = [URLS[name] for name in args.urls]
    proc = launch_chromium(urls)

    controller = kb.Controller()

    def send_ctrl_tab(shift: bool = False) -> None:
        """Simulate Ctrl+Tab (optionally with Shift) using xdotool if available."""
        cmd = ["xdotool", "key", "--clearmodifiers", "ctrl+"]
        cmd[-1] += "shift+Tab" if shift else "Tab"
        try:
            subprocess.run(cmd, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            controller.press(kb.Key.ctrl)
            if shift:
                controller.press(kb.Key.shift)
            controller.press(kb.Key.tab)
            controller.release(kb.Key.tab)
            if shift:
                controller.release(kb.Key.shift)
            controller.release(kb.Key.ctrl)

    def show_button():
        root = Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        size = 40
        screen_height = root.winfo_screenheight()
        root.geometry(f"{size}x{size}+0+{screen_height - size}")

        def on_click():
            send_ctrl_tab()

        btn = Button(root, text="\u21c6", command=on_click)
        btn.pack(fill="both", expand=True)
        root.mainloop()

    def on_press(key):
        if key == kb.Key.f5:
            send_ctrl_tab()
        elif key == kb.Key.f6:
            send_ctrl_tab(shift=True)

    listener = kb.Listener(on_press=on_press)
    listener.start()

    button_thread = None
    if not args.no_button:
        button_thread = threading.Thread(target=show_button, daemon=True)
        button_thread.start()

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
