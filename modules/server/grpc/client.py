# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import grpc

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtWebKitWidgets
from PyQt5.QtCore import Qt

import kiosk_pb2
import kiosk_pb2_grpc

if __name__ == '__main__':
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = kiosk_pb2_grpc.KioskStub(channel)

        print(stub.ping(kiosk_pb2.Ping(
            name='localhost',
            data='test',
            ip='10.42.0.1',
        )))

        screenshot = stub.screenshot(kiosk_pb2.Request(
            auth='TeßtC0de!1',
            command=kiosk_pb2.Command(
                data='',
                code=''
            ) 
        ))
        imageRaw = QtCore.QByteArray(screenshot.data)
        image = QtGui.QImage.fromData(imageRaw, 'PNG')
        image.save('screenshot.png', 'PNG')
        
        print(stub.command(kiosk_pb2.Request(
            auth='TeßtC0de!1',
            command=kiosk_pb2.Command(
                #data='https://zabbix.fitbase.de/screens.php?elementId=25',
                data='https://google.com',

                code='open'
            ) 
        )))
