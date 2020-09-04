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
from gevent.pywsgi import WSGIServer


class Server(QtCore.QThread):
    command = QtCore.pyqtSignal(object)
    screenshot = QtCore.pyqtSignal(object)
    ping = QtCore.pyqtSignal(object)

    @inject.params(config='config', controller='api.controller')
    def run(self, config, controller):

        try:

            host = config.get('server.host')
            port = config.get('server.port')

            http_server = WSGIServer(
                (host, int(port)), controller
            )
            http_server.serve_forever()

        except KeyboardInterrupt:
            print('Server stopped by user.')
