# DisplayPi

This repository contains a small program to display a web page in full screen on Raspberry Pi OS (64‑bit). By default it opens `https://www.flightradar24.com/42.74,-1.57/8`. The script monitors the page and reloads it only when loading fails.

## Requirements
- Raspberry Pi OS 64‑bit with graphical environment
- Python 3
- `chromium-browser`
- `requests` Python package

Install Chromium if it is not already available:
```bash
sudo apt-get update
sudo apt-get install -y chromium-browser
```
Install the ``requests`` package if it is missing:
```bash
pip3 install requests
```

## Usage
1. Copy this repository to `/home/pi/DisplayPi` on your Raspberry Pi.
2. Optionally edit `displaypi.py` to change the URL.
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
Edit `displaypi.py` if you want to change the URL or tweak how often the script
checks that the page loaded correctly. Modify `CHECK_SECONDS` to change the
verification interval.
