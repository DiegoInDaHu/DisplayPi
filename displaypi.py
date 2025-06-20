#!/usr/bin/env python3
"""DisplayPi - simple kiosk launcher using Chromium.

This simple script opens a single URL in fullscreen (kiosk) mode using the
``chromium-browser`` application that comes with Raspberry Pi OS.
"""

import subprocess

import RPi.GPIO as GPIO

# URLs to display
URL_1 = "https://www.flightradar24.com/simple/"
URL_2 = "http://localhost:3000"

# GPIO pin where the button is connected
BUTTON_PIN = 27


CHROMIUM_CMD = [
    "chromium-browser",
    "--noerrdialogs",
    "--kiosk",
]


def launch_chromium(urls: list[str]) -> subprocess.Popen:
    """Launch Chromium pointing to ``urls`` in kiosk mode."""
    cmd = CHROMIUM_CMD + urls
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def switch_tab(tab_index: int) -> None:
    """Use ``xdotool`` to switch to ``tab_index`` (1-based)."""
    subprocess.run(
        ["xdotool", "key", f"ctrl+{tab_index}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def main() -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    proc = launch_chromium([URL_1, URL_2])
    current_tab = 1  # Chromium opens the first URL as tab 1

    def handle_button(channel: int) -> None:
        nonlocal current_tab
        # Toggle between tab 1 and 2
        current_tab = 2 if current_tab == 1 else 1
        switch_tab(current_tab)

    GPIO.add_event_detect(
        BUTTON_PIN, GPIO.FALLING, callback=handle_button, bouncetime=300
    )

    try:
        proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    main()
