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
# WITHOUT WARRANTIES OR CONDITION
import os
import glob


class Device(object):
    """
    
    """


class CPU(Device):
    def __init__(self, path="/sys/devices/system/cpu/"):
        """

        :param path: 
        """
        self._path = path

    def __devices(self):
        """

        :return: 
        """
        for device in glob.glob('%s/cpu[0-9]' % self._path):
            yield device

    def status(self):
        """

        :return: 
        """
        for device in self.__devices():
            for result in glob.glob('%s/cpufreq/scaling_governor' % device):
                if not os.path.isfile(result):
                    continue
                with open(result, 'r') as stream:
                    yield stream.read().strip("\n")

    def powersafe(self):
        """

        :return: 
        """
        pass

    def perfomance(self):
        """

        :return: 
        """
        pass
