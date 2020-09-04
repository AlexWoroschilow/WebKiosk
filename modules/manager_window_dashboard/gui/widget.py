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
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .button import ButtonFlat
from .button import ButtonPicture
from .button import IconButton
from .label import LabelSubtitle
from .thread import DashboardEntityThread


class HostEntityProtocol(QtWidgets.QWidget):

    def __init__(self):
        super(HostEntityProtocol, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        self.layout.addWidget(self.spacer)

        self.widgets = []

    def append(self, protocol, open=False):
        if self.spacer is not None and self.spacer:
            self.layout.removeWidget(self.spacer)

        label = QtWidgets.QLabel(protocol)
        label.setMaximumHeight(30)
        color = "green" if open else "red"
        label.setStyleSheet(
            'QWidget { color: #ffffff; padding: 0px 5px; font-size: 16px; background-color: %s; }' % color)
        self.widgets.append(label)

        self.layout.addWidget(label, 0, Qt.AlignLeft)

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        self.layout.addWidget(self.spacer)


class DashboardEntity(QtWidgets.QWidget):
    openAction = QtCore.pyqtSignal(object)
    removeAction = QtCore.pyqtSignal(object)
    saveAction = QtCore.pyqtSignal(object)

    def __init__(self, host=None):
        super(DashboardEntity, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.host = host

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(LabelSubtitle(host.name), 0, 0, 1, 3)

        self.button = IconButton(QtGui.QIcon('img/trash'))
        self.button.clicked.connect(lambda x: self.removeAction.emit(host))
        self.layout.addWidget(self.button, 0, 2, 1, 1)

        self.pixmap = QtGui.QPixmap('img/desktop.png')
        if host.screenshot is not None and host.screenshot:
            self.pixmap.loadFromData(QtCore.QByteArray().fromRawData(host.screenshot))

        self.button = ButtonPicture(self.pixmap.scaled(300, 400, Qt.KeepAspectRatioByExpanding))
        self.button.clicked.connect(lambda x: self.openAction.emit(host))
        self.layout.addWidget(self.button, 1, 0, 3, 3)

        self.protocols = HostEntityProtocol()
        self.layout.addWidget(self.protocols, 3, 0, 1, 3)

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
        if not screenshot: return None
        self.host.screenshot = screenshot
        storage.update(self.host)

        self.pixmap.loadFromData(self.host.screenshot)
        self.button.setPixmap(self.pixmap.scaled(300, 400, Qt.KeepAspectRatio))


class DashboardWidget(QtWidgets.QWidget):
    openAction = QtCore.pyqtSignal(object)
    removeAction = QtCore.pyqtSignal(object)
    refreshAction = QtCore.pyqtSignal(object)
    saveAction = QtCore.pyqtSignal(object)

    @inject.params(storage='storage')
    def __init__(self, storage):
        super(DashboardWidget, self).__init__()
        from .scroll import DashboardWidgetScrollArea

        self.widgets = []

        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.buttonUpdate = ButtonFlat('Refresh')
        self.buttonUpdate.clicked.connect(self.removeAction.emit)
        self.layout.addWidget(self.buttonUpdate, 0, 0, 1, 1)

        self.dashboard = DashboardWidgetScrollArea()
        self.dashboard.openAction.connect(self.openAction.emit)
        self.dashboard.removeAction.connect(self.removeAction.emit)
        self.dashboard.saveAction.connect(self.saveAction.emit)

        self.layout.addWidget(self.dashboard, 1, 0, 1, 6)

    @inject.params(storage='storage', host='storage.host')
    def onActionHostSave(self, scanned=None, storage=None, window=None, host=None):
        host.ip = scanned.ip
        host.screenshot = scanned.screenshot
        host.name = scanned.name
        storage.append(host)
        self.dashboard.refresh()

    @inject.params(storage='storage', host='storage.host')
    def onActionHostRemove(self, scanned=None, storage=None, window=None, host=None):
        storage.remove(scanned)

        self.dashboard.refresh()
