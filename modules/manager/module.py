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

from lib.plugin import Loader

from .gui.window import ManagerWindow 
from .gui.button import ButtonFlat


class Loader(Loader):

    @property
    def enabled(self):
        return not hasattr(self._options, 'server')

    def config(self, binder=None):
        binder.bind_to_constructor('manager', self.__window)
        binder.bind_to_provider('manager_scanner', self.__scanner)
        binder.bind_to_provider('manager_dashboard', self.__dashboard)
        binder.bind_to_provider('manager_device', self.__device)
 
    @inject.params(widget='manager_dashboard')
    def __window(self, widget=None):

        window = ManagerWindow()
        window.setCentralWidget(widget)
        
        action = functools.partial(self.onActionHostOpen, window=window)
        widget.open.connect(action)
        action = functools.partial(self.onActionHostSave, window=window)
        widget.save.connect(action)

        scanner = ButtonFlat('Scanner')
        window.statusBar().addWidget(scanner)
        scanner.clicked.connect(functools.partial(
            self.onActionScaner, window=window
        ))

        dashboard = ButtonFlat('Dashboard')
        window.statusBar().addWidget(dashboard)
        dashboard.clicked.connect(functools.partial(
            self.onActionDashboard, window=window
        ))

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
    def onActionHostOpen(self, data, manager, window):
        widget = manager.instance(data)
        window.setCentralWidget(widget)
        widget.back.connect(functools.partial(
            self.onActionDashboard, window=window
        ))

    def onActionHostSave(self, data, window):
        print(data, window)

    @inject.params(widget='manager_scanner')
    def onActionScaner(self, event=None, widget=None, window=None):
        
        action = functools.partial(self.onActionHostOpen, window=window)
        widget.open.connect(action)
        action = functools.partial(self.onActionHostSave, window=window)
        widget.save.connect(action)
        action = functools.partial(self.onActionDashboard, window=window)
        widget.back.connect(action)

        window.setCentralWidget(widget)

    @inject.params(widget='manager_dashboard')
    def onActionDashboard(self, event=None, widget=None, window=None):
        
        action = functools.partial(self.onActionHostOpen, window=window)
        widget.open.connect(action)
        action = functools.partial(self.onActionHostSave, window=window)
        widget.save.connect(action)

        window.setCentralWidget(widget)

