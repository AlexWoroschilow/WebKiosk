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

from .service import NetworkScanner


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def configure(self, binder, options, args):
        binder.bind_to_constructor('network_scanner.service', self.__service)
        binder.bind_to_constructor('network_scanner', self.__thread)

    def __service(self):
        return NetworkScanner()

    @inject.params(scanner='network_scanner.service')
    def __thread(self, scanner):
        return ScannerThread(scanner)


class ScannerThread(QtCore.QThread):
    started = QtCore.pyqtSignal(object)
    status = QtCore.pyqtSignal(object)
    closed = QtCore.pyqtSignal(object)
    found = QtCore.pyqtSignal(object)
    stoped = QtCore.pyqtSignal(object)

    def __init__(self, scanner):
        super(ScannerThread, self).__init__()
        self.scanner = scanner
        self.network = None
        self.ports = None

    @inject.params(logger='logger')
    def scan(self, network=None, ports=[('rest', 52312), ], logger=None):
        logger.info('[scanner] scanning: {}'.format(network, ports))
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
            self.found.emit((ip, protocol, result))
        self.stoped.emit((self.network, self.ports))
