#! /usr/bin/python3
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
import os

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

import sys
import inject
import logging
import optparse

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from lib.kernel import Kernel


class Application(QtWidgets.QApplication):

    def __init__(self, options=None, args=None):
        super(Application, self).__init__(sys.argv)
        
        self.kernel = Kernel(options, args)
        self.kernel.application = self

    @inject.params(config='config', manager='manager')
    def exec_(self, config=None, manager=None):

        manager.show()

        return super(Application, self).exec_()


if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option("--manager-config", default='./kiosk.conf', dest="config", help="Config file location")
    parser.add_option("--manager-logfile", default='./kiosk.log', dest="logfile", help="Logfile location")
    parser.add_option("--manager-loglevel", default=logging.DEBUG, dest="loglevel", help="Logging level")
    
    (options, args) = parser.parse_args()
    
    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_())

