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

import time
import inject
import socket
import netifaces

from PyQt5 import QtCore
from PyQt5 import QtGui

from lib.plugin import Loader

from .service import NetworkScanner


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('network_scanner.service', self.__service)
        binder.bind_to_constructor('network_scanner', self.__thread)
 
    def __service(self):
        return NetworkScanner()

    @inject.params(scanner='network_scanner.service')
    def __thread(self, scanner):
        return ScannerThread(scanner)


class ScannerThread(QtCore.QThread):
    started = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal(object)
    status = QtCore.pyqtSignal(object)
    closed = QtCore.pyqtSignal(object)
    open = QtCore.pyqtSignal(object)

    def __init__(self, scanner):
        super(ScannerThread, self).__init__()
        self.scanner = scanner
        self.network = None
        self.ports = None

    def scan(self, network=None, ports=None):
        self.network = network
        self.ports = ports
        self.start()
        
    def stop(self):
        self.scanner.stop()

    def pause(self):
        self.scanner.pause()
        
    def resume(self):
        self.scanner.resume()

    def run(self):

        self.started.emit((self.network, self.ports))
        for result in self.scanner.scan(self.network, self.ports):
            if result is None:
                continue
            ip, protocol, result = result
            self.status.emit((ip, protocol, result))
            if result not in ['SUCCESS']: 
                self.closed.emit((ip, protocol, result))
                continue
            self.open.emit((ip, protocol, result))
        self.finished.emit((self.network, self.ports))

