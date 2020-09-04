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
from modules.manager.gui import dashboard


class Loader(Loader):

    @property
    def enabled(self):
        return not hasattr(self._options, 'server')

    def config(self, binder=None):
        binder.bind_to_constructor('manager', self.__window)
        binder.bind_to_provider('manager_scanner', self.__scanner)
        binder.bind_to_provider('manager_dashboard', self.__dashboard)
        binder.bind_to_provider('manager_device', self.__device)
 
    @inject.params(scanner='manager_scanner', dashboard='manager_dashboard')
    def __window(self, scanner=None, dashboard=None):

        window = ManagerWindow()

        container = QtWidgets.QSplitter()
        window.setCentralWidget(container)

        scanner.open.connect(functools.partial(self.onActionHostOpen, window=window))
        scanner.save.connect(functools.partial(dashboard.onActionHostSave, window=window))
        
        dashboard.open.connect(functools.partial(self.onActionHostOpen, window=window))
        dashboard.save.connect(functools.partial(dashboard.onActionHostSave, window=window))

        container.addWidget(scanner)
        container.addWidget(dashboard)

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

        scanner.started.connect(widget.onActionScanningStart)
        scanner.found.connect(widget.onActionScanningFound)
        scanner.status.connect(widget.onActionScanningStatus)
        scanner.stoped.connect(widget.onActionScanningStop)
        
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
        
        action = functools.partial(self.onActionDashboard, window=window)
        widget.back.connect(action)

    @inject.params(widget1='manager_scanner', widget2='manager_dashboard')
    def onActionDashboard(self, window, widget1=None, widget2=None):

        container = QtWidgets.QSplitter()
        window.setCentralWidget(container)

        widget1.open.connect(functools.partial(self.onActionHostOpen, window=window))
        widget1.save.connect(functools.partial(widget2.onActionHostSave, window=window))
        
        widget2.open.connect(functools.partial(self.onActionHostOpen, window=window))
        widget2.save.connect(functools.partial(widget2.onActionHostSave, window=window))

        container.addWidget(widget1)
        container.addWidget(widget2)

        return window

