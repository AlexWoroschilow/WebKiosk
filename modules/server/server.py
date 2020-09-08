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
import os


class Server(QtCore.QThread):
    command = QtCore.pyqtSignal(object)
    screenshot = QtCore.pyqtSignal(object)
    ping = QtCore.pyqtSignal(object)

    @inject.params(config='config', controller='api.controller')
    def run(self, config, controller):

        try:

            host = config.get('server.host', '0.0.0.0')
            port = config.get('server.port', '52312')

            key = config.get('certificate.key', 'ssl/localhost.key')
            if not key: raise Exception('Certificate key not found: {}'.format(key))
            if not os.path.exists(key): raise Exception('Certificate key not found: {}'.format(key))

            crt = config.get('certificate.crt', 'ssl/localhost.crt')
            if not crt: raise Exception('Certificate not found: {}'.format(key))
            if not os.path.exists(crt): raise Exception('Certificate not found: {}'.format(key))

            http_server = WSGIServer(
                (host, int(port)), controller,
                keyfile=key, certfile=crt
            )
            http_server.serve_forever()

        except KeyboardInterrupt:
            print('Server stopped by user.')
