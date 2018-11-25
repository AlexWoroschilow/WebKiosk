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
import grpc
import time
import inject
from concurrent import futures
from PyQt5 import QtCore

from lib.plugin import Loader

from .grpc import kiosk_pb2_grpc 
from .service import KioskServicer
from .service import KioskClientManager


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('grpc_client_manager', self.__client)
        if hasattr(self._options, 'server') and self._options.server:
            binder.bind_to_constructor('grpc_service', self.__service)
            binder.bind_to_constructor('grpc_server', self.__server)

    @inject.params(server='grpc_server')
    def __service(self, server):
        return KioskServicer(server)        

    @inject.params(config='config')
    def __server(self, config):
        return Server()        

    @inject.params(config='config')
    def __client(self, config):
        return KioskClientManager()        


class Server(QtCore.QThread):

    command = QtCore.pyqtSignal(object)
    screenshot = QtCore.pyqtSignal(object)
    ping = QtCore.pyqtSignal(object)

    @inject.params(config='config', grpc_service='grpc_service')
    def run(self, config, grpc_service):

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        kiosk_pb2_grpc.add_KioskServicer_to_server(grpc_service, server)
        
        server.add_insecure_port('{}:{}'.format(
            config.get('server.host'),
            config.get('server.port'),
        ))
        
        server.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop(0)
