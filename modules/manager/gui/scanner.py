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

from .list import HostList
from .button import ButtonFlat


class ScannerWidget(QtWidgets.QWidget):
    
    back = QtCore.pyqtSignal(object)
    open = QtCore.pyqtSignal(object)
    save = QtCore.pyqtSignal(object)
    
    scanStart = QtCore.pyqtSignal(object)
    scanStop = QtCore.pyqtSignal(object)
    scanResume = QtCore.pyqtSignal(object)
    scanPause = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, config):
        super(ScannerWidget, self).__init__()

        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        
        button = ButtonFlat('Back')
        button.clicked.connect(lambda x: self.back.emit(x))
        self.layout.addWidget(button, 0, 0, 1, 1)

        self.mask = QtWidgets.QLineEdit()
        self.mask.returnPressed.connect(self.onActionStart)
        self.mask.setPlaceholderText('192.168.1.0/24')
        self.mask.setText(config.get('scanner.network'))
        self.layout.addWidget(self.mask, 0, 1, 1, 3)
        
        self.start = ButtonFlat('Scan')
        self.start.clicked.connect(self.onActionStart)
        self.layout.addWidget(self.start, 0, 4, 1, 1)
        self.start.setVisible(True)

        self.stop = ButtonFlat('Stop')
        self.stop.clicked.connect(self.onActionStop)
        self.layout.addWidget(self.stop, 0, 4, 1, 1)
        self.stop.setVisible(False)

        self.pause = ButtonFlat('Pause')
        self.pause.clicked.connect(self.onActionPause)
        self.layout.addWidget(self.pause, 0, 3, 1, 1)
        self.pause.setVisible(False)

        self.resume = ButtonFlat('Resume')
        self.resume.clicked.connect(self.onActionResume)
        self.layout.addWidget(self.resume, 0, 3, 1, 1)
        self.resume.setVisible(False)
        
        self.list = HostList()
        self.list.open.connect(lambda x: self.open.emit(x))
        self.list.save.connect(lambda x: self.save.emit(x))
        self.list.back.connect(lambda x: self.back.emit(x))

        self.layout.addWidget(self.list, 1, 0, 1, 5)

    @inject.params(config='config')
    def onActionStart(self, event, config):
        config.set('scanner.network', self.mask.text())
        self.scanStart.emit(self.mask.text())
        self.start.setVisible(False)
        self.pause.setVisible(True)
        self.stop.setVisible(True)
        self.resume.setVisible(False)

    def onActionStop(self, event):
        self.scanStop.emit(self.mask.text())
        self.start.setVisible(True)
        self.pause.setVisible(False)
        self.stop.setVisible(False)
        self.resume.setVisible(False)

    def onActionPause(self, event):
        self.scanPause.emit(self.mask.text())
        self.start.setVisible(False)
        self.stop.setVisible(True)
        self.pause.setVisible(False)
        self.resume.setVisible(True)

    def onActionResume(self, event):
        self.scanResume.emit(self.mask.text())
        self.start.setVisible(False)
        self.stop.setVisible(True)
        self.resume.setVisible(False)
        self.pause.setVisible(True)

    def onHostOpen(self, host):
        self.list.addHost(host)

    def onHostStatus(self, data):
        print(data)

