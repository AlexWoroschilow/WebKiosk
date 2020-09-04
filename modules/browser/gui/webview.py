#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inject
from PyQt5 import QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import netifaces


class KioskWebView(QtWebEngineWidgets.QWebEngineView):
    commandAction = QtCore.pyqtSignal(object)
    pageAction = QtCore.pyqtSignal(object)
    screenshotAction = QtCore.pyqtSignal(object)
    pingAction = QtCore.pyqtSignal(object)

    screenshots = []

    @inject.params(config='config')
    def __init__(self, config=None):
        super(KioskWebView, self).__init__()
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.ip)

        profile_default: QtWebEngineWidgets.QWebEngineProfile = self.page().profile()
        profile_default.setPersistentCookiesPolicy(QtWebEngineWidgets.QWebEngineProfile.ForcePersistentCookies)
        profile_default.setPersistentStoragePath(config.get('browser.cookies'))
        profile_default.setCachePath(config.get('browser.cache'))

        self.screenshotAction.connect(self.screenshotEvent)
        self.pageAction.connect(self.pageEvent)

    @property
    def ip(self):
        addresses = []
        for iface in netifaces.interfaces():
            for data in netifaces.ifaddresses(iface).setdefault(netifaces.AF_INET, [{'addr': None}]):
                if data['addr'] not in [None, '127.0.0.1']:
                    addresses.append(data['addr'])
        return " ".join(addresses)

    def command(self, command):
        if command.code in ['open', 'url', 'link']:
            self.load(QtCore.QUrl(command.data))

    def screenshotEvent(self, event=None):
        self.screenshots.append(self.screenshot)

    def pageEvent(self, event=None):
        if 'url' not in event.keys():
            return None

        url = event['url']
        if not len(url):
            return

        self.load(QtCore.QUrl(url))

    @property
    def screenshot(self):
        page: QtWebEngineWidgets.QWebEnginePage = self.page()
        page.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.ScreenCaptureEnabled, True)

        image = QtGui.QImage(page.contentsSize().toSize(), QtGui.QImage.Format_ARGB32)
        painter = QtGui.QPainter(image)

        self.render(painter)
        painter.end()

        imageRaw = QtCore.QByteArray()
        buffer = QtCore.QBuffer(imageRaw)
        buffer.open(QtCore.QIODevice.WriteOnly)
        image.save(buffer, 'PNG')

        return imageRaw.data()

    def get_screenshot_latest(self):
        import time
        counter = 0
        while not len(self.screenshots):
            if counter > 60:
                return None
            time.sleep(0.5)
            counter += 1

        screenshot = self.screenshots.pop()
        return screenshot

    def ping(self, entity):
        print(entity)
