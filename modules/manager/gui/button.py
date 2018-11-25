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


class ButtonFlat(QtWidgets.QPushButton):
    
    def __init__(self, name):
        super(ButtonFlat, self).__init__(name)
        self.setFlat(True)


class ButtonPicture(QtWidgets.QAbstractButton):

    def __init__(self, pixmap, parent=None):
        super(ButtonPicture, self).__init__(parent)
        self.pixmap = pixmap

    def setPixmap(self, pixmap):
        self.pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
