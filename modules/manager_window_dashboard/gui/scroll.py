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
from PyQt5.QtCore import Qt

from .widget import DashboardEntity


class DashboardWidgetScrollAreaItem(QtWidgets.QListWidgetItem):

    def __init__(self, entity=None):
        super(DashboardWidgetScrollAreaItem, self).__init__()
        self.setSizeHint(QtCore.QSize(250, 250))
        self.setTextAlignment(Qt.AlignCenter)
        self.setData(0, entity)


class DashboardWidgetScrollArea(QtWidgets.QListWidget):
    openAction = QtCore.pyqtSignal(object)
    removeAction = QtCore.pyqtSignal(object)
    saveAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DashboardWidgetScrollArea, self).__init__()
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setViewMode(QtWidgets.QListWidget.IconMode)

        self.refresh()

    @inject.params(storage='storage')
    def refresh(self, storage):
        self.clear()
        for entity in storage.hosts:
            self.addItemRow(entity)

    def addItemRow(self, entity):
        item = DashboardWidgetScrollAreaItem(entity)
        self.addItem(item)

        widget = DashboardEntity(entity)
        widget.openAction.connect(self.openAction.emit)
        widget.removeAction.connect(self.removeAction.emit)
        widget.saveAction.connect(self.saveAction.emit)

        widget.start()
        self.setItemWidget(item, widget)
