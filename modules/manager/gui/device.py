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
        self.image.setPixmap(self.pixmap.scaled(self.width(), self.height()))

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)        
        scrollArea.setWidget(self.image)

        self.layout.addWidget(scrollArea, 1, 0, 1, 7)

        client = manager.instance(self.host, '50051')
        status = client.status()
        if status is None:
            return None
        
        self.url.setText(status.url)
        self.screeshot(status.screenshot)

    def screeshot(self, screenshot=None):
        if screenshot is None:
            return None
        
        self.pixmap.loadFromData(screenshot.data)
        self.image.setPixmap(self.pixmap.scaled(self.width(), self.height()))
        self.image.resize(self.width(), self.height())

    def resizeEvent(self, event):
        self.image.setPixmap(self.pixmap.scaled(self.width(), self.height()))
        self.image.resize(self.width(), self.height())

    @inject.params(manager='grpc_client_manager')
    def onActionUrlSend(self, event=None, manager=None):
        client = manager.instance(self.host, '50051')
        if not len(self.url.text()):
            return None
        client.url(self.url.text())
        self.screeshot(client.screenshot())

    @inject.params(manager='grpc_client_manager')
    def onActionRefresh(self, event, manager):
        client = manager.instance(self.host, '50051')
        self.screeshot(client.screenshot())


