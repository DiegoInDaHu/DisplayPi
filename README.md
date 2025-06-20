# DisplayPi

This repository contains a small program to display a web page in full screen on Raspberry Pi OS (64‑bit). By default it opens `https://www.flightradar24.com/simple/`.

## Requirements
- Raspberry Pi OS 64‑bit with graphical environment
- Python 3
- `chromium-browser`
- `xdotool`
- `RPi.GPIO` (usually installed by default on Raspberry Pi OS)

Install Chromium if it is not already available:
```bash
sudo apt-get update
sudo apt-get install -y chromium-browser
sudo apt-get install -y xdotool python3-rpi.gpio
```

## Usage
1. Copy this repository to `/home/pi/DisplayPi` on your Raspberry Pi.
2. Optionally edit `displaypi.py` to change the URLs.
3. Install the systemd service:

```bash
sudo cp displaypi.service /etc/systemd/system/displaypi.service
sudo systemctl daemon-reload
sudo systemctl enable displaypi.service
sudo systemctl start displaypi.service
```

The service will launch the web viewer on boot. To stop it:

```bash
sudo systemctl stop displaypi.service
```

## Customization
`displaypi.py` launches Chromium in kiosk mode with two tabs. A push button
connected to GPIO 27 toggles between them. Edit the script if you need to change
the URLs or adjust how Chromium is launched.
