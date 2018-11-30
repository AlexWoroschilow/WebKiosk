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


class HostEntityProtocol(QtWidgets.QWidget):

    def __init__(self, collection=[]):
        super(HostEntityProtocol, self).__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        for name in collection:
            label = LabelText(name)
            self.layout.addWidget(label, 0, Qt.AlignLeft)
            
        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        self.layout.addWidget(self.spacer)

    def append(self, collection=[]):
        self.layout.removeWidget(self.spacer)
        for name in collection:
            label = LabelText(name)
            self.layout.addWidget(label, 0, Qt.AlignLeft)

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        self.layout.addWidget(self.spacer)


class HostEntity(QtWidgets.QWidget):
    
    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)

    def __init__(self, host):
        super(HostEntity, self).__init__()

        self.layout = QtWidgets.QGridLayout()

        self.layout.addWidget(LabelTitle("{}".format(host.name)), 0, 0)
        self.layout.addWidget(LabelText("{}".format(host.ip)), 1, 0)
        
        button = ButtonFlat('Open')
        self.layout.addWidget(button, 0, 1)
        button.clicked.connect(lambda x: self.open.emit(host))

        button = ButtonFlat('Update')
        self.layout.addWidget(button, 1, 1)
        button.clicked.connect(lambda x: self.save.emit(host))

        self.setLayout(self.layout)


class HostList(QtWidgets.QListWidget):
    
    back = QtCore.pyqtSignal(object)
    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    
    @inject.params(storage='storage')
    def __init__(self, storage):
        super(HostList, self).__init__()
        self.setStyleSheet("QListWidget::item {border: none; min-height: 80px; }");
        for host in storage.scanned:
            self.addHost(host)
    
    def addHost(self, host=None):
        if host is None or not host:
            return None
        
        item = QtWidgets.QListWidgetItem()
        item.widget = HostEntity(host)
        item.widget.open.connect(lambda x: self.open.emit(x))
        item.widget.save.connect(self.onActionUpdate)

        self.addItem(item)

        self.setItemWidget(item, item.widget)

    @inject.params(storage='storage', manager='grpc_client_manager')
    def onActionUpdate(self, host, storage, manager):
        client = manager.instance(host.ip)
        if client is None or not client:
            return None

        screenshot = client.screenshot()
        if screenshot is None or not screenshot:
            return None
        
        host.screenshot = screenshot.data
        storage.update(host)
        
        self.save.emit(host)
