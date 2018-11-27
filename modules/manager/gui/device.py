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
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .button import ButtonFlat


class DeviceWidgetManager(object):

    def instance(self, host):
        return DeviceWidget(host)


class DeviceWidget(QtWidgets.QWidget):

    back = QtCore.pyqtSignal()

    @inject.params(manager='grpc_client_manager')    
    def __init__(self, host, manager=None):
        super(DeviceWidget, self).__init__()
        self.thread = DeviceThread(manager)

        self.host = host

        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.url = QtWidgets.QLineEdit()
        self.url.returnPressed.connect(self.onActionUrlSend)

        button = ButtonFlat('Back')
        button.clicked.connect(lambda x: self.back.emit())
        self.layout.addWidget(button, 0, 0, 1, 1)
        
        self.url.setPlaceholderText('http://...')
        self.layout.addWidget(self.url, 0, 1, 1, 5)
        
        button = ButtonFlat('Send')
        button.clicked.connect(self.onActionUrlSend)
        self.layout.addWidget(button, 0, 5, 1, 1)
        
        button = ButtonFlat('Refresh')
        button.clicked.connect(self.onActionRefresh)
        self.layout.addWidget(button, 0, 6, 1, 1)
        
        self.pixmap = QtGui.QPixmap('img/progress.jpg')
        self.image = QtWidgets.QLabel()
        self.image.setPixmap(self.pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio))

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidget(self.image)

        self.layout.addWidget(scrollArea, 1, 0, 1, 7)

        self.thread.status.connect(self.status) 
        self.thread.start(self.host)

    def status(self, status=None):
        if status is None:
            return None

        self.url.setText(status.url)
        self.pixmap.loadFromData(status.screenshot.data)
        self.image.setPixmap(self.pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio))
        self.image.resize(self.width(), self.height())

    def resizeEvent(self, event):
        self.image.setPixmap(self.pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio))
        self.image.resize(self.width(), self.height())

    @inject.params(manager='grpc_client_manager')
    def onActionUrlSend(self, event=None, manager=None):
        if not len(self.url.text()):
            return None
        client = manager.instance(self.host, 50051)
        self.status(client.url(self.url.text()))

    def onActionRefresh(self, event=None):
        self.thread.start(self.host)


class DeviceThread(QtCore.QThread):

    status = QtCore.pyqtSignal(object)

    def __init__(self, manager):
        super(DeviceThread, self).__init__()
        self.manager = manager
        self.hosts = None
        self.port = 50051

    def start(self, host=None):
        self.host = host
        super(DeviceThread, self).start()
        
    def run(self):
        client = self.manager.instance(self.host, self.port)
        if client is not None and client:
            self.status.emit(client.status())

