#!/usr/bin/env python3
"""DisplayPi - simple kiosk launcher using Chromium.

This simple script opens a single URL in fullscreen (kiosk) mode using the
``chromium-browser`` application that comes with Raspberry Pi OS. It monitors
the page and reloads it only when a load failure is detected.
"""

import subprocess
import time
import requests

# URL to display
URL = "https://www.flightradar24.com/42.74,-1.57/8"

# Seconds between checks to verify that the page loaded correctly. When the
# check fails, Chromium is restarted to reload the page.
CHECK_SECONDS = 30

CHROMIUM_CMD = [
    "chromium-browser",
    "--noerrdialogs",
    "--kiosk",
]


def launch_chromium(url: str) -> subprocess.Popen:
    """Launch Chromium pointing to ``url`` in kiosk mode."""
    cmd = CHROMIUM_CMD + [url]
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def page_loaded(url: str) -> bool:
    """Return ``True`` if ``url`` is reachable (HTTP 200)."""
    try:
        resp = requests.get(url, timeout=10)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def main() -> None:
    proc = launch_chromium(URL)

    try:
        while True:
            time.sleep(CHECK_SECONDS)
            if not page_loaded(URL):
                proc.terminate()
                proc.wait()
                proc = launch_chromium(URL)
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    main()
