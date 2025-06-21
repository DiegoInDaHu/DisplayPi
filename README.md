# DisplayPi

This repository contains a small program to display one or more web pages in fullscreen on Raspberry Pi OS (64‑bit). By default it opens all predefined pages (`flightradar` and `local`).

## Requirements
- Raspberry Pi OS 64‑bit with graphical environment
- Python 3
- `chromium-browser`
- `pynput` Python package (install with `pip install -r requirements.txt`)
- `keyboard` Python package (install with `pip install -r requirements.txt`)
- `xdotool` (install with `sudo apt-get install -y xdotool`)

Install Chromium if it is not already available:
```bash
sudo apt-get update
sudo apt-get install -y chromium-browser
```

## Usage
1. Copy this repository to `/home/pi/DisplayPi` on your Raspberry Pi.
2. Run `displaypi.py --urls local` to display only the local page or omit the option to load all available pages as tabs.
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
Use the `--urls` argument to select which predefined pages are opened as tabs. While Chromium is running press **F5** to switch to the next tab and **F6** to go back. Edit `displaypi.py` if you want to add more URLs or adjust how Chromium is launched.
By default a small button appears in the lower left corner that performs the same action as **Ctrl+Tab** to quickly cycle through the opened tabs. The implementation relies on `xdotool` to send the shortcut. Use the `--no-button` option if you prefer to hide it.
If `xdotool` is not available the script falls back to the `keyboard` package to
emit the shortcut.
