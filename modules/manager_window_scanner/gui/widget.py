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
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from .button import ButtonFlat
from .button import IconButton
from .label import LabelText
from .label import LabelTitle
from .thread import HostListEntityThread


class HostEntityProtocol(QtWidgets.QWidget):

    def __init__(self):
        super(HostEntityProtocol, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.spacer)

        self.widgets = []

    def append(self, protocol, open=False):
        if self.spacer is not None and self.spacer:
            self.layout.removeWidget(self.spacer)

        label = QtWidgets.QLabel(protocol)
        color = "green" if open else "red"
        label.setStyleSheet(
            'QWidget { color: #ffffff; padding: 0px 5px; font-size: 16px; background-color: %s; }' % color)
        self.widgets.append(label)

        self.layout.addWidget(label, 0, Qt.AlignLeft)

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.layout.addWidget(self.spacer)

    def clean(self):
        for widget in self.widgets:
            self.layout.removeWidget(widget)


class HostListEntity(QtWidgets.QWidget):
    openAction = QtCore.pyqtSignal(object)
    removeAction = QtCore.pyqtSignal(object)
    saveAction = QtCore.pyqtSignal(object)

    def __init__(self, host):
        super(HostListEntity, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setContentsMargins(10, 0, 0, 0)
        self.layout.addWidget(LabelTitle(host.name), 0, 0, 1, 9)
        self.layout.addWidget(LabelText(host.ip), 1, 0)

        self.protocols = HostEntityProtocol()
        self.layout.addWidget(self.protocols, 2, 0, 1, 9)

        button = IconButton(QtGui.QIcon('img/preview'))
        button.clicked.connect(lambda x: self.openAction.emit(host))
        self.layout.addWidget(button, 0, 10)

        button = IconButton(QtGui.QIcon('img/save'))
        button.clicked.connect(lambda x: self.saveAction.emit(host))
        self.layout.addWidget(button, 1, 10)

        button = IconButton(QtGui.QIcon('img/trash'))
        button.clicked.connect(lambda x: self.removeAction.emit(host))
        self.layout.addWidget(button, 2, 10)

        self.setLayout(self.layout)

        self.thread = HostListEntityThread(host.ip)
        self.thread.protocol.connect(self.protocol)
        self.thread.start()

    def protocol(self, data):
        name, port, status = data
        self.protocols.append(name, status == 'SUCCESS')
