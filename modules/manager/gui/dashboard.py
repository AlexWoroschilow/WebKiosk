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
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from .button import ButtonPicture
from .button import ButtonFlat

from .label import LabelSubtitle


class DashboardWidget(QtWidgets.QWidget):

    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    
    @inject.params(storage='storage')
    def __init__(self, storage):
        super(DashboardWidget, self).__init__()
        
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        layout = QtWidgets.QGridLayout()
        widgetCentral = QtWidgets.QWidget()
        widgetCentral.setLayout(layout)

        refresh = ButtonFlat('Refresh')
        self.layout.addWidget(refresh, 0, 0, 1, 1)

        for i, chunk in enumerate(self.chunks(storage.hosts, 3)):
            for j, host in enumerate(chunk):
                widget = DashboardEntity(host)
                widget.open.connect(lambda x: self.open.emit(x))
                widget.save.connect(lambda x: self.open.emit(x))
                layout.addWidget(widget, i, j)
                
                refresh.clicked.connect(widget.refresh)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)        
        scrollArea.setWidget(widgetCentral)
        
        self.layout.addWidget(scrollArea, 1, 0, 1, 6)

    def chunks(self, li, n):
        if li == []:
            return
        yield li[:n]
        yield from self.chunks(li[n:], n)


class DashboardEntity(QtWidgets.QWidget):
    
    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    
    def __init__(self, host=None):
        super(DashboardEntity, self).__init__()
        self.setMinimumWidth(200)
        self.setMinimumHeight(150)
        self.thread = DashboardEntityThread(host.ip)
        self.thread.screenshot.connect(self.screenshot)

        self.host = host

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(LabelSubtitle("{} ({})".format(host.name, host.ip)))

        self.pixmap = QtGui.QPixmap('img/desktop.png')
        if host.screenshot is not None and host.screenshot:
            self.pixmap.loadFromData(QtCore.QByteArray().fromRawData(host.screenshot))
        
        self.button = ButtonPicture(self.pixmap.scaled(200, 150, Qt.KeepAspectRatio))
        self.button.clicked.connect(lambda x: self.open.emit(host))
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
        self.thread.start()

    @inject.params(storage='storage')
    def screenshot(self, screenshot, storage=None):
        if screenshot is None or not screenshot:
            return None
        
        self.host.screenshot = screenshot 
        storage.update(self.host)
        
        self.pixmap.loadFromData(self.host.screenshot)
        self.button.setPixmap(self.pixmap.scaled(200, 150, Qt.KeepAspectRatio))

    def refresh(self, event=None):
        if self.thread is not None and self.thread:
            self.thread.start()


class DashboardEntityThread(QtCore.QThread):

    screenshot = QtCore.pyqtSignal(object)

    def __init__(self, ip):
        super(DashboardEntityThread, self).__init__()
        self.ip = ip
        
    @inject.params(manager='grpc_client_manager')
    def run(self, manager=None):
        client = manager.instance(self.ip, 50051)
        if client is None or not client:
            return None
        screenshot = client.screenshot()
        if screenshot is not None and screenshot:
            self.screenshot.emit(screenshot.data)
