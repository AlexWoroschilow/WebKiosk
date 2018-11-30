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
import functools

from PyQt5 import QtWidgets

from lib.plugin import Loader

from .gui.window import ManagerWindow 


class Loader(Loader):

    @property
    def enabled(self):
        return not hasattr(self._options, 'server')

    def config(self, binder=None):
        binder.bind_to_constructor('manager', self.__window)
        binder.bind_to_provider('manager_scanner', self.__scanner)
        binder.bind_to_provider('manager_dashboard', self.__dashboard)
        binder.bind_to_provider('manager_device', self.__device)
 
    @inject.params(widget1='manager_scanner', widget2='manager_dashboard')
    def __window(self, widget1=None, widget2=None):

        window = ManagerWindow()

        container = QtWidgets.QSplitter()
        window.setCentralWidget(container)

        widget1.open.connect(functools.partial(self.onActionHostOpen, window=window))
        widget1.save.connect(functools.partial(self.onActionHostSave, window=window))
        
        widget2.open.connect(functools.partial(self.onActionHostOpen, window=window))
        widget2.save.connect(functools.partial(self.onActionHostSave, window=window))

        container.addWidget(widget1)
        container.addWidget(widget2)

        return window
    
    def __dashboard(self):
        from .gui.dashboard import DashboardWidget
        widget = DashboardWidget()
        
        return widget
    
    @inject.params(scanner='network_scanner', config='config')
    def __scanner(self, scanner=None, config=None):
        from .gui.scanner import ScannerWidget

        widget = ScannerWidget()
        widget.scanStart.connect(scanner.scan)
        widget.scanPause.connect(scanner.pause)
        widget.scanResume.connect(scanner.resume)
        widget.scanStop.connect(scanner.stop)

        scanner.open.connect(widget.onHostOpen)
        scanner.status.connect(widget.onHostStatus)
        
        return widget    
    
    @inject.params(scanner='network_scanner')
    def __device(self, scanner=None):
        from .gui.device import DeviceWidgetManager
        return DeviceWidgetManager()

    @inject.params(manager='manager_device')
    def onActionHostOpen(self, host, manager, window):
        if host is None or not host:
            return None
        
        widget = manager.instance(host)
        if widget is None or not widget:
            return None
        
        window.setCentralWidget(widget)
        
        widget.back.connect(functools.partial(
            self.onActionDashboard, window=window
        ))

    def onActionHostSave(self, data, window):
        print(data, window)

    @inject.params(widget1='manager_scanner', widget2='manager_dashboard')
    def onActionDashboard(self, window, widget1=None, widget2=None):

        container = QtWidgets.QSplitter()
        window.setCentralWidget(container)

        widget1.open.connect(functools.partial(self.onActionHostOpen, window=window))
        widget1.save.connect(functools.partial(self.onActionHostSave, window=window))
        
        widget2.open.connect(functools.partial(self.onActionHostOpen, window=window))
        widget2.save.connect(functools.partial(self.onActionHostSave, window=window))

        container.addWidget(widget1)
        container.addWidget(widget2)

        return window

