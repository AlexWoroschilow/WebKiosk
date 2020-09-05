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

from .widget import HostListEntity


class HostList(QtWidgets.QListWidget):
    backAction = QtCore.pyqtSignal(object)
    openAction = QtCore.pyqtSignal(object)
    removeAction = QtCore.pyqtSignal(object)
    saveAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(HostList, self).__init__()
        self.setMinimumWidth(300)
        self.refresh()

    @inject.params(storage='storage')
    def refresh(self, event=None, storage=None):
        self.clear()
        for host in storage.scanned:
            self.addHost(host)

    def addHost(self, host=None):
        if host is None or not host:
            return None

        widget = HostListEntity(host)
        widget.openAction.connect(self.openAction.emit)
        widget.removeAction.connect(self.removeAction.emit)
        widget.saveAction.connect(self.saveAction.emit)
        widget.removeAction.connect(self.refresh)

        item = QtWidgets.QListWidgetItem()

        self.addItem(item)

        self.setItemWidget(item, widget)

        self.item
