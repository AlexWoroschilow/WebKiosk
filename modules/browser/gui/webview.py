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
from PyQt5 import QtCore
from PyQt5 import QtWebKitWidgets

from .cookie import PersistentCookieJar


class KioskWebView(QtWebKitWidgets.QWebView):

    def __init__(self, destination=None):
        super(KioskWebView, self).__init__()
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.cookieJar = PersistentCookieJar(destination)

        self.cookieJar.load()
        
        self.loadFinished.connect(self.cookieJar.dump)
        
        self.page().networkAccessManager().setCookieJar(self.cookieJar)
        self.cookieJar.setParent(self)

    def command(self, command):
        if command.code in ['open', 'url', 'link']:
            self.load(QtCore.QUrl(command.data))

    def screenshot(self, entity):
        print(entity)

    def ping(self, entity):
        print(entity)
