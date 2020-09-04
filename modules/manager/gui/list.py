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

from .button import ButtonFlat
from .label import LabelTitle
from .label import LabelText
from .widget import HostEntityProtocol


class HostList(QtWidgets.QListWidget):
    
    back = QtCore.pyqtSignal(object)
    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    
    @inject.params(storage='storage')
    def __init__(self, storage):
        super(HostList, self).__init__()
        self.setStyleSheet("QListWidget::item { border: none; min-height: 90px; }");
        for host in storage.scanned:
            self.addHost(host)
    
    def addHost(self, host=None):
        if host is None or not host:
            return None
        
        item = QtWidgets.QListWidgetItem()
        item.widget = HostListEntity(host)
        item.widget.open.connect(lambda x: self.open.emit(x))
        item.widget.save.connect(lambda x: self.save.emit(x))

        self.addItem(item)

        self.setItemWidget(item, item.widget)


class HostListEntity(QtWidgets.QWidget):
    
    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)    

    def __init__(self, host):
        super(HostListEntity, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setContentsMargins(10, 0, 0, 0)
        self.layout.addWidget(LabelTitle("{}".format(host.name)), 0, 0, 1, 10)
        self.layout.addWidget(LabelText("{}".format(host.ip)), 1, 0)
        
        self.protocols = HostEntityProtocol()
        self.layout.addWidget(self.protocols, 2, 0, 1, 10)
        
        button = ButtonFlat('Open')
        self.layout.addWidget(button, 0, 10)
        button.clicked.connect(lambda x: self.open.emit(host))

        button = ButtonFlat('Append')
        self.layout.addWidget(button, 1, 10)
        button.clicked.connect(lambda x: self.save.emit(host))

        self.setLayout(self.layout)
        
        self.thread = HostListEntityThread(host.ip)
        self.thread.protocol.connect(self.protocol)
        self.thread.start()
        
    def protocol(self, data):
        name, port, status = data
        self.protocols.append(name, status == 'SUCCESS')


class HostListEntityThread(QtCore.QThread):

    protocol = QtCore.pyqtSignal(object)

    def __init__(self, ip):
        super(HostListEntityThread, self).__init__()
        self.ip = ip
        
    @inject.params(scanner='network_scanner.service')
    def run(self, scanner=None):
        for result in scanner.scan(self.ip, [('ssh', 22), ('grcp', 50051), ('x11vnc', 5900)]):
            ip, (protocol, port), status = result
            self.protocol.emit((protocol, port, status))
