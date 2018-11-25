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

from .button import ButtonFlat
from .button import ButtonPicture
from .label import LabelText


class DashboardEntity(QtWidgets.QWidget):
    
    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    
    @inject.params(manager='grpc_client_manager')    
    def __init__(self, host=None, manager=None):
        super(DashboardEntity, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(LabelText(host))

        self.pixmap = QtGui.QPixmap('img/progress.jpg')
        self.button = ButtonPicture(self.pixmap.scaled(200, 200))
        self.button.clicked.connect(lambda x: self.open.emit((host)))
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

        client = manager.instance(host, '50051')
        self.screeshot(client.screenshot())

    def screeshot(self, screenshot=None):
        if screenshot is None:
            return None
        self.pixmap.loadFromData(screenshot.data)
        self.button.setPixmap(self.pixmap.scaled(200, 200))


class DashboardWidget(QtWidgets.QWidget):

    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    
    def __init__(self):
        super(DashboardWidget, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        layout = QtWidgets.QGridLayout()
        widget1 = QtWidgets.QWidget()
        widget1.setLayout(layout)

        for i, chunk in enumerate(self.chunks(self.hosts(), 3)):
            for j, host in enumerate(chunk):
                widget = DashboardEntity(host)
                widget.open.connect(lambda x: self.open.emit(x))
                widget.save.connect(lambda x: self.open.emit(x))
                layout.addWidget(widget, i, j)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)        
        scrollArea.setWidget(widget1)
        
        self.layout.addWidget(scrollArea)

    def chunks(self, li, n):
        if li == []:
            return
        yield li[:n]
        yield from self.chunks(li[n:], n)

    def hosts(self):
        return ['192.168.1.75', '10.42.0.3']        

