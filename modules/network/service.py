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
import IPy
import time

import socket
import errno
from socket import gethostbyname, gaierror


class NetworkScanner(object):
    
    _pause = False
    _stop = False
    
    def stop(self):
        self._stop = True
        self._pause = False

    def pause(self):
        self._pause = True
        self._stop = False

    def resume(self):
        self._pause = False
        self._stop = False

    def open(self, host=None, port=None):
        if host is None or port is None:
            return None
        try:
            socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
    
            response = socket_obj.connect_ex((host, int(port)))
            socket_obj.close()
            return (response == 0)
        except gaierror:
            return False
        return False
    
    def scan(self, network='192.168.1.0/24', ports=None):
        self._pause = False
        self._stop = False
        if ports is None or not ports:
            ports = [('ssh', 22), ('grcp', 50051), ('x11vnc', 5900)]

        for ip_address in IPy.IP(network):

            if self._pause == True:
                time.sleep(1)
                yield None
                continue

            if self._stop == True:
                break
        
            for bunch in ports:
                protocol, port = bunch
                if self._pause == True:
                    time.sleep(1)
                    yield None
                    continue

                if self._stop == True:
                    break

                socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
        
                response = socket_obj.connect_ex((str(ip_address), port))
                socket_obj.close()
                
                if response == 0:
                    yield (str(ip_address), (protocol, port), 'SUCCESS')
                    continue
        
                yield (str(ip_address), (protocol, port), errno.errorcode[response])

            
if __name__ == "__main__":
    scanner = NetworkScanner()
    for result in scanner.scan():
        ip, protocol, result = result
        if result not in ['SUCCESS']: 
            print('.')
            continue
        print(ip, protocol, result)
        
