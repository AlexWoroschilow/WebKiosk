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
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class ButtonFlat(QtWidgets.QPushButton):

    def __init__(self, name):
        super(ButtonFlat, self).__init__(name)
        self.setMaximumWidth(50)
        self.setFlat(True)


class IconButton(QtWidgets.QPushButton):
    def __init__(self, icon=None, text=None):
        super(IconButton, self).__init__(icon, None)
        self.setToolTipDuration(0)
        self.setMaximumWidth(30)
        self.setToolTip(text)
        self.setFlat(True)

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(5)
            effect.setOffset(0)
            self.setGraphicsEffect(effect)

        if QEvent.type() == QtCore.QEvent.Leave:
            self.setGraphicsEffect(None)

        return super(IconButton, self).event(QEvent)
