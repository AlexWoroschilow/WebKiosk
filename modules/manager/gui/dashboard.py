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

from .label import LabelText


class DashboardWidget(QtWidgets.QWidget):

    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    
    @inject.params(manager='grpc_client_manager')
    def __init__(self, manager):
        super(DashboardWidget, self).__init__()
        self.thread = DashboardThread(manager)
        
        self.collection = []
        
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        layout = QtWidgets.QGridLayout()
        widget1 = QtWidgets.QWidget()
        widget1.setLayout(layout)

        for i, chunk in enumerate(self.chunks(self.hosts, 3)):
            for j, host in enumerate(chunk):
                widget = DashboardEntity(host)
                layout.addWidget(widget, i, j)
                self.collection.append((host, widget))

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)        
        scrollArea.setWidget(widget1)
        
        self.layout.addWidget(scrollArea, 1, 0, 1, 6)

        self.thread.screenshot.connect(self.screenshot) 
        self.thread.start(self.hosts)

        self.refresh = ButtonFlat('Refresh')
        self.refresh.clicked.connect(lambda x: self.thread.start(self.hosts))
        self.layout.addWidget(self.refresh, 0, 0, 1, 1)

    @property
    def hosts(self):
        return [
            '192.168.1.88',
            '192.168.1.101',
            '192.168.1.135',
            '192.168.1.208',
            '192.168.1.242',
            '192.168.1.253',
            '192.168.1.176',
        ]        

    def screenshot(self, data):
        host_required, screenshot = data
        for bunch in self.collection:
            host, widget = bunch
            if host not in [host_required]:
                continue
            widget.screeshot(screenshot)
            widget.open.connect(lambda x: self.open.emit(x))
            widget.save.connect(lambda x: self.open.emit(x))

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
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(LabelText(host))

        self.pixmap = QtGui.QPixmap('img/desktop.png')
        self.button = ButtonPicture(self.pixmap.scaled(300, 200, Qt.KeepAspectRatio))
        self.button.clicked.connect(lambda x: self.open.emit((host)))
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def screeshot(self, screenshot=None):
        if screenshot is None:
            return None
        if screenshot.data is not None:
            self.pixmap.loadFromData(screenshot.data)
            self.button.setPixmap(self.pixmap.scaled(300, 200, Qt.KeepAspectRatio))


class DashboardThread(QtCore.QThread):

    screenshot = QtCore.pyqtSignal(object)

    def __init__(self, manager):
        super(DashboardThread, self).__init__()
        self.manager = manager

        self.hosts = None
        self.port = 50051

    def start(self, hosts=None):
        self.hosts = hosts
        super(DashboardThread, self).start()
        
    def run(self):
        for host in self.hosts:
            client = self.manager.instance(host, self.port)
            if client is not None and client:
                self.screenshot.emit((host, client.screenshot()))
