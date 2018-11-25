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
import functools

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtGui

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

    def __init__(self, response):
        super(HostEntity, self).__init__()
        self.address, (self.name, self.port), self.status = response

        self.layout = QtWidgets.QGridLayout()

        self.layout.addWidget(LabelTitle("{}".format(self.address)), 0, 0)
        
        self.protocols = HostEntityProtocol([self.name.capitalize()])
        self.layout.addWidget(self.protocols, 1, 0)
        
        button = ButtonFlat('Open')
        self.layout.addWidget(button, 0, 1)
        button.clicked.connect(lambda x: self.open.emit(self.address))

        button = ButtonFlat('Save')
        self.layout.addWidget(button, 1, 1)
        button.clicked.connect(lambda x: self.save.emit(self.address))

        self.setLayout(self.layout)

    def append(self, response):
        address, (name, port), status = response
        self.protocols.append([name.capitalize()])

    def hasIp(self, address):
        return address == self.address


class HostList(QtWidgets.QListWidget):
    
    back = QtCore.pyqtSignal(object)
    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    
    def __init__(self):
        super(HostList, self).__init__()
        self.setStyleSheet("QListWidget::item {border: none; min-height: 80px; }");
    
    def getItemByHost(self, ip):
        for i in range(self.count()):
            item = self.item(i)
            widget = item.widget
            if widget.hasIp(ip):
                return (item, widget) 
        return None
            
    def addHost(self, host):
        address, (name, port), status = host
        
        existed = self.getItemByHost(address)
        if existed is not None:
            item, widget = existed
            widget.append(host)
            return None
        
        item = QtWidgets.QListWidgetItem()
        self.addItem(item)
        
        item.widget = HostEntity(host)
        item.widget.open.connect(self.onActionItemOpen)
        item.widget.save.connect(self.onActionItemSave)

        self.setItemWidget(item, item.widget)

    def onActionItemOpen(self, event=None):
        self.open.emit(event)

    def onActionItemSave(self, event=None):
        self.save.emit(event)
