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
import math

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from .button import ButtonPicture
from .button import ButtonFlat
from .label import LabelSubtitle
from .label import LabelTitle
from .label import LabelText

from .widget import HostEntityProtocol


class DashboardWidgetScrollAreaContent(QtWidgets.QWidget):

    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)

    @inject.params(storage='storage')
    def __init__(self, columns, storage):
        super(DashboardWidgetScrollAreaContent, self).__init__()

        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        def chunks(li, n):
            if li == []:
                return
            yield li[:n]
            yield from chunks(li[n:], n)
        
        pool = []
        for i, chunk in enumerate(chunks(storage.hosts, columns)):
            for j, host in enumerate(chunk):
                widget = DashboardEntity(host)
                widget.open.connect(lambda x: self.open.emit(x))
                widget.save.connect(lambda x: self.open.emit(x))
                
                layout.addWidget(widget, i, j)
                
                pool.append(widget)
                
        for widget in pool:
            widget.start()


class DashboardWidgetScrollArea(QtWidgets.QScrollArea):

    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)

    columns = 3
    
    def __init__(self):
        super(DashboardWidgetScrollArea, self).__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.central = DashboardWidgetScrollAreaContent(self.columns)
        self.central.open.connect(lambda x: self.open.emit(x))
        self.central.save.connect(lambda x: self.open.emit(x))
        self.setWidget(self.central)

    def resizeEvent(self, event):
        columns = math.floor(event.size().width() / 210)
        if columns == self.columns:
            return super(DashboardWidgetScrollArea, self).resizeEvent(event)
        
        self.columns = columns 
        self.central = DashboardWidgetScrollAreaContent(self.columns)
        self.central.open.connect(lambda x: self.open.emit(x))
        self.central.save.connect(lambda x: self.open.emit(x))
        self.setWidget(self.central)
        
        return super(DashboardWidgetScrollArea, self).resizeEvent(event)


class DashboardWidget(QtWidgets.QWidget):

    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    
    @inject.params(storage='storage')
    def __init__(self, storage):
        super(DashboardWidget, self).__init__()
        self.widgets = []
        
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.buttonUpdate = ButtonFlat('Refresh')
        self.layout.addWidget(self.buttonUpdate, 0, 0, 1, 1)
        
        self.dashboard = DashboardWidgetScrollArea()
        self.dashboard.open.connect(lambda x: self.open.emit(x))
        self.dashboard.save.connect(lambda x: self.open.emit(x))

        self.layout.addWidget(self.dashboard, 1, 0, 1, 6)

    @inject.params(storage='storage', host='storage.host')
    def onActionHostSave(self, scanned=None, storage=None, window=None, host=None):
        host.ip = scanned.ip
        host.screenshot = scanned.screenshot
        host.name = scanned.name
        storage.append(host)
        
        self.dashboard = DashboardWidgetScrollArea()
        self.dashboard.open.connect(lambda x: self.open.emit(x))
        self.dashboard.save.connect(lambda x: self.open.emit(x))
        self.layout.addWidget(self.dashboard, 1, 0, 1, 6)


class DashboardEntity(QtWidgets.QWidget):
    
    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    
    def __init__(self, host=None):
        super(DashboardEntity, self).__init__()
        self.setMinimumWidth(200)
        self.setMinimumHeight(150)
        self.host = host

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(LabelSubtitle("{} ({})".format(host.name, host.ip)))

        self.pixmap = QtGui.QPixmap('img/desktop.png')
        if host.screenshot is not None and host.screenshot:
            self.pixmap.loadFromData(QtCore.QByteArray().fromRawData(host.screenshot))
        
        self.button = ButtonPicture(self.pixmap.scaled(200, 150, Qt.KeepAspectRatio))
        self.button.clicked.connect(lambda x: self.open.emit(host))
        self.layout.addWidget(self.button)

        self.protocols = HostEntityProtocol()
        self.layout.addWidget(self.protocols)

        self.setLayout(self.layout)
        
    def start(self):
        self.thread = DashboardEntityThread(self.host.ip)
        self.thread.screenshot.connect(self.screenshot)
        self.thread.protocol.connect(self.protocol)
        self.thread.start()

    def protocol(self, data):
        name, port, status = data
        self.protocols.append(name, status == 'SUCCESS')

    @inject.params(storage='storage')
    def screenshot(self, screenshot, storage=None):
        if screenshot is None or not screenshot:
            return None
        
        self.host.screenshot = screenshot 
        storage.update(self.host)
        
        self.pixmap.loadFromData(self.host.screenshot)
        self.button.setPixmap(self.pixmap.scaled(200, 150, Qt.KeepAspectRatio))

    def refresh(self, event=None):
        self.protocols.clean()
        if self.thread is not None and self.thread:
            self.thread.start()


class DashboardEntityThread(QtCore.QThread):

    screenshot = QtCore.pyqtSignal(object)
    protocol = QtCore.pyqtSignal(object)

    def __init__(self, ip):
        super(DashboardEntityThread, self).__init__()
        self.ip = ip
        
    @inject.params(manager='grpc_client_manager', scanner='network_scanner.service')
    def run(self, manager=None, scanner=None):
        client = manager.instance(self.ip, 50051)
        if client is None or not client:
            return None
        screenshot = client.screenshot()
        if screenshot is not None and screenshot:
            self.screenshot.emit(screenshot.data)
        for result in scanner.scan(self.ip, [('ssh', 22), ('grcp', 50051), ('x11vnc', 5900)]):
            ip, (protocol, port), status = result
            self.protocol.emit((protocol, port, status))

