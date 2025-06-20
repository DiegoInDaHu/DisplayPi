#!/usr/bin/env python3
"""DisplayPi - simple full-screen web viewer for Raspberry Pi OS.

Edit the URLS list below to change which websites are shown.
The application cycles through the URLs in full screen mode.
"""

import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

# List of URLs to display
URLS = [
    "https://www.flightradar24.com",
    # Add more URLs here
]

# Seconds to wait before showing the next URL. Set to 0 to disable rotation.
INTERVAL_SECONDS = 60

class Browser(QtWidgets.QMainWindow):
    def __init__(self, urls, interval):
        super().__init__()
        self.urls = urls
        self.index = 0
        self.interval = interval
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.view)
        self.load_current_url()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.next_url)
        if self.interval > 0 and len(self.urls) > 1:
            self.timer.start(self.interval * 1000)
        self.showFullScreen()

    def load_current_url(self):
        self.view.load(QtCore.QUrl(self.urls[self.index]))

    def next_url(self):
        self.index = (self.index + 1) % len(self.urls)
        self.load_current_url()


def main():
    app = QtWidgets.QApplication(sys.argv)
    browser = Browser(URLS, INTERVAL_SECONDS)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
