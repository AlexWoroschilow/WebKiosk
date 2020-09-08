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
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import netifaces

from .webview import KioskWebView


class BrowserContainer(QtWidgets.QWidget):
    commandAction = QtCore.pyqtSignal(object)
    pageAction = QtCore.pyqtSignal(object)
    screenshotAction = QtCore.pyqtSignal(object)
    pingAction = QtCore.pyqtSignal(object)

    def __init__(self, browser):
        super(BrowserContainer, self).__init__()

        self.setLayout(QtWidgets.QGridLayout())
        self.browser: KioskWebView = browser

        self.pageAction.connect(self.browser.pageAction.emit)
        self.commandAction.connect(self.browser.commandAction.emit)
        self.screenshotAction.connect(self.browser.screenshotAction.emit)
        self.pingAction.connect(self.browser.pingAction.emit)

        self.layout().addWidget(self.browser, 0, 0)

    @property
    def ip(self):
        return self.browser.ip

    def load(self, url):
        return self.browser.load(url)

    @property
    def screenshot(self):
        return self.browser.screenshot

    def command(self, command):
        return self.browser.command(command)

    def screenshotEvent(self, event=None):
        return self.browser.screenshotEvent(event)

    def pageEvent(self, event=None):
        return self.browser.pageEvent(event)

    def get_screenshot_latest(self):
        return self.browser.get_screenshot_latest()

    def ping(self, entity):
        return self.browser.ping(entity)
