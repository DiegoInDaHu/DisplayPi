# DisplayPi

This repository contains a small program to display web pages in full screen on Raspberry Pi OS (64‑bit). It starts with `https://www.flightradar24.com` and can rotate through additional URLs if you add them to the script.

## Requirements
- Raspberry Pi OS 64‑bit with graphical environment
- Python 3
- `chromium-browser`

Install Chromium if it is not already available:
```bash
sudo apt-get update
sudo apt-get install -y chromium-browser
```

## Usage
1. Copy this repository to `/home/pi/DisplayPi` on your Raspberry Pi.
2. Optionally edit `displaypi.py` and add more URLs in the `URLS` list.
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
- To change the time between URL changes, edit `INTERVAL_SECONDS` in
  `displaypi.py`.
- Set `INTERVAL_SECONDS` to `0` to disable automatic rotation.
