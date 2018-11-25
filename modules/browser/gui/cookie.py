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
import os

from PyQt5 import QtNetwork


class PersistentCookieJar(QtNetwork.QNetworkCookieJar):

    def __init__(self, destination=None):
        super(PersistentCookieJar, self).__init__()
        self.destination = destination

    def dump(self, event=None):
        self.save()

    def load(self):
        if not os.path.exists(self.destination):
            return None
        with open(self.destination, 'r') as stream:
            content = bytes(stream.read(), 'utf-8')
            self.setAllCookies(QtNetwork.QNetworkCookie.parseCookies(content)) 
            stream.close()

    def save(self):
        with open(self.destination, 'w+') as stream: 
            for cookie in self.allCookies():
                qba = cookie.toRawForm()
                stream.write(str(qba.data(), encoding='utf-8'))
            stream.close()

