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


class HostListEntityThread(QtCore.QThread):
    protocol = QtCore.pyqtSignal(object)

    def __init__(self, ip):
        super(HostListEntityThread, self).__init__()
        self.ip = ip

    @inject.params(scanner='network_scanner.service')
    def run(self, scanner=None):
        for result in scanner.scan(self.ip, [('ssh', 22), ('rest', 52312), ('x11vnc', 5900)]):
            ip, (protocol, port), status = result
            self.protocol.emit((protocol, port, status))
