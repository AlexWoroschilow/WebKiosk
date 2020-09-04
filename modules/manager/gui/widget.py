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
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets


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
        color = "green" if open else "red"
        label.setStyleSheet('QWidget { color: #ffffff; padding: 0px 5px; font-size: 16px; background-color: %s; }' % color);
        self.widgets.append(label)
        
        self.layout.addWidget(label, 0, Qt.AlignLeft)

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
        self.layout.addWidget(self.spacer)

    def clean(self):
        for widget in self.widgets:
            self.layout.removeWidget(widget)
