#!/usr/bin/env python3
"""DisplayPi - simple kiosk launcher using Chromium.

This script opens a list of URLs in fullscreen (kiosk) mode using the
`chromium-browser` application that comes with Raspberry Pi OS.  The
browser window is restarted for each URL when rotation is enabled.
"""

import subprocess
import time
from typing import List

# List of URLs to display
URLS: List[str] = [
    "https://www.flightradar24.com/42.74,-1.57/8",
    # Add more URLs here
]

# Seconds to wait before showing the next URL. Set to 0 to disable rotation.
INTERVAL_SECONDS = 60

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
    index = 0
    proc = launch_chromium(URLS[index])

    try:
        while True:
            if INTERVAL_SECONDS <= 0 or len(URLS) == 1:
                # Wait forever if rotation is disabled.
                proc.wait()
                break
            time.sleep(INTERVAL_SECONDS)
            proc.terminate()
            proc.wait()
            index = (index + 1) % len(URLS)
            proc = launch_chromium(URLS[index])
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    main()
