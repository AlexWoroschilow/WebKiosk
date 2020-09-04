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
import grpc
import inject
import socket
import netifaces

from PyQt5 import QtCore
from PyQt5 import QtGui

from .grpc import kiosk_pb2 
from .grpc import kiosk_pb2_grpc 
from builtins import int


class KioskClientManager(object):

    def instance(self, server='localhost', port='50051'):
        return KioskClient(server, port) 


class KioskClient(object):
    server = None
    port = None

    def __init__(self, server='localhost', port='50051'):
        self.server = server
        self.port = port

    @inject.params(logger='logger')
    def ping(self, logger=None):
        try:
            with grpc.insecure_channel('{}:{}'.format(self.server, self.port)) as channel:
                stub = kiosk_pb2_grpc.KioskStub(channel)
                return stub.ping(kiosk_pb2.Ping(
                    name='localhost',
                    data='test',
                    ip='10.42.0.1',
                ))
        except grpc._channel._Rendezvous:
            logger.error('Server unavailable: {}:{}'.format(self.server, self.port))
        return None

    @inject.params(config='config', logger='logger')
    def screenshot(self, config=None, logger=None):
        try:
            with grpc.insecure_channel('{}:{}'.format(self.server, self.port)) as channel:
                stub = kiosk_pb2_grpc.KioskStub(channel)
                return stub.screenshot(kiosk_pb2.Request(
                    auth=config.get('security.code'),
                    command=kiosk_pb2.Command(
                        data='',
                        code=''
                    ) 
                ))
        except (grpc._channel._Rendezvous, grpc._channel._InactiveRpcError) as ex:
            logger.error('Server unavailable: {}:{}, {}'.format(self.server, self.port, ex))
        return None

    @inject.params(config='config', logger='logger')
    def status(self, config=None, logger=None):
        try:
            with grpc.insecure_channel('{}:{}'.format(self.server, self.port)) as channel:
                stub = kiosk_pb2_grpc.KioskStub(channel)
                return stub.status(kiosk_pb2.Request(
                    auth=config.get('security.code'),
                    command=kiosk_pb2.Command(
                        data='', code=''
                    ) 
                ))
        except (grpc._channel._Rendezvous, grpc._channel._InactiveRpcError) as ex:
            logger.error('Server unavailable: {}:{}'.format(self.server, self.port))
        return None

    @inject.params(config='config', logger='logger')
    def url(self, url=None, config=None, logger=None):
        try:
            with grpc.insecure_channel('{}:{}'.format(self.server, self.port)) as channel:
                stub = kiosk_pb2_grpc.KioskStub(channel)
                return stub.command(kiosk_pb2.Request(
                    auth=config.get('security.code'),
                    command=kiosk_pb2.Command(
                        code='url', data=url
                    ) 
                ))
        except (grpc._channel._Rendezvous, grpc._channel._InactiveRpcError) as ex:
            logger.error('Server unavailable: {}:{}'.format(self.server, self.port))
        return None


class KioskServicer(kiosk_pb2_grpc.KioskServicer):

    def __init__(self, application):
        self.application = application

    def _network_data_ip(self):
        addresses = []
        for iface in netifaces.interfaces():
            for data in netifaces.ifaddresses(iface).setdefault(netifaces.AF_INET, [{'addr': None}]):
                if data['addr'] not in [None, '127.0.0.1']:
                    addresses.append(data['addr'])
        return ', '.join(addresses)

    def _network_data(self):
        response = []
        for iface in netifaces.interfaces():
            addresses = []
            for data in netifaces.ifaddresses(iface).setdefault(netifaces.AF_INET, [{'addr':'No IP'}]):
                addresses.append(data['addr'])
            response.append('{}: {}'.format(iface, ', '.join(addresses)))
        return "\n".join(response)

    @inject.params(config='config')
    def command(self, request, context, config):
        
        if request.command.code in ['open', 'url', 'link']:
            self.application.command.emit(request.command)
            config.set('browser.url', request.command.data)

        return self.status(request, context)

    def ping(self, request, context):
        
        return kiosk_pb2.Pong(
            name=socket.gethostname(),
            data=self._network_data(),
            ip=self._network_data_ip()
        )
                
    @inject.params(browser='browser')
    def screenshot(self, request, context, browser):
        frame = browser.page().mainFrame()

        image = QtGui.QImage(browser.page().viewportSize(), QtGui.QImage.Format_ARGB32)
        painter = QtGui.QPainter(image)
        frame.render(painter)
        painter.end()
        
        imageRaw = QtCore.QByteArray()
        buffer = QtCore.QBuffer(imageRaw)
        buffer.open(QtCore.QIODevice.WriteOnly)
        image.save(buffer, 'PNG')
        
        return kiosk_pb2.Screenshot(
            data=imageRaw.data(),
            timestamp=int(time.time()),
        )
                
    @inject.params(browser='browser', config='config')
    def status(self, request, context, browser, config):
        frame = browser.page().mainFrame()

        image = QtGui.QImage(browser.page().viewportSize(), QtGui.QImage.Format_ARGB32)
        painter = QtGui.QPainter(image)
        frame.render(painter)
        painter.end()
        
        imageRaw = QtCore.QByteArray()
        buffer = QtCore.QBuffer(imageRaw)
        buffer.open(QtCore.QIODevice.WriteOnly)
        image.save(buffer, 'PNG')
        
        return kiosk_pb2.Status(
            ip=self._network_data_ip(),
            url=config.get('browser.url'),
            timestamp=int(time.time()),
            screenshot=kiosk_pb2.Screenshot(
                timestamp=int(time.time()),
                data=imageRaw.data()
            )
        )

