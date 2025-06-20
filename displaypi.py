#!/usr/bin/env python3
"""DisplayPi - simple kiosk launcher using Chromium.

This simple script opens a single URL in fullscreen (kiosk) mode using the
``chromium-browser`` application that comes with Raspberry Pi OS.
"""

import subprocess

# URL to display
URL = "https://www.flightradar24.com/42.74,-1.57/8"


CHROMIUM_CMD = [
    "chromium-browser",
    "--noerrdialogs",
    "--kiosk",
]


def launch_chromium(url: str) -> subprocess.Popen:
    """Launch Chromium pointing to ``url`` in kiosk mode."""
    cmd = CHROMIUM_CMD + [url]
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def main() -> None:
    proc = launch_chromium(URL)

    try:
        proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    main()
