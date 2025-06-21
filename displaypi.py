#!/usr/bin/env python3
"""DisplayPi - simple kiosk launcher using Chromium.

This simple script opens a single URL in fullscreen (kiosk) mode using the
``chromium-browser`` application that comes with Raspberry Pi OS.
"""

import argparse
import subprocess


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


def launch_chromium(url: str) -> subprocess.Popen:
    """Launch Chromium pointing to ``url`` in kiosk mode."""
    cmd = CHROMIUM_CMD + [url]
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch Chromium in kiosk mode")
    parser.add_argument(
        "--url",
        choices=URLS.keys(),
        default="flightradar",
        help="Which page to display",
    )
    args = parser.parse_args()

    url = URLS[args.url]
    proc = launch_chromium(url)

    try:
        proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    main()
