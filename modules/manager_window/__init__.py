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
import functools

import inject
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options, args):
        return not hasattr(options, 'server')

    def configure(self, binder, options, args):
        binder.bind_to_constructor('manager', self.__window)

    @inject.params(scanner='manager_scanner', dashboard='manager_dashboard')
    def __window(self, scanner=None, dashboard=None):
        from .gui.window import ManagerWindow

        window = ManagerWindow()

        container = QtWidgets.QSplitter(Qt.Horizontal)
        container.setContentsMargins(0, 0, 0, 0)

        window.setCentralWidget(container)

        scanner.open.connect(functools.partial(self.onActionHostOpen, window=window))
        scanner.save.connect(functools.partial(dashboard.onActionHostSave, window=window))

        dashboard.openAction.connect(functools.partial(self.onActionHostOpen, window=window))
        dashboard.removeAction.connect(functools.partial(dashboard.onActionHostRemove, window=window))
        dashboard.saveAction.connect(functools.partial(dashboard.onActionHostSave, window=window))

        container.addWidget(scanner)
        container.addWidget(dashboard)

        container.setStretchFactor(0, 1)
        container.setStretchFactor(1, 4)

        return window

    @inject.params(scanner='manager_scanner', dashboard='manager_dashboard')
    def onActionDashboard(self, window, scanner=None, dashboard=None):

        container = QtWidgets.QSplitter(Qt.Horizontal)
        container.setContentsMargins(0, 0, 0, 0)

        window.setCentralWidget(container)

        scanner.open.connect(functools.partial(self.onActionHostOpen, window=window))
        scanner.save.connect(functools.partial(dashboard.onActionHostSave, window=window))

        dashboard.openAction.connect(functools.partial(self.onActionHostOpen, window=window))
        dashboard.removeAction.connect(functools.partial(dashboard.onActionHostRemove, window=window))
        dashboard.saveAction.connect(functools.partial(dashboard.onActionHostSave, window=window))

        container.addWidget(scanner)
        container.addWidget(dashboard)

        container.setStretchFactor(0, 1)
        container.setStretchFactor(1, 4)

        return window

    @inject.params(manager='manager_device')
    def onActionHostOpen(self, host, manager, window):
        if not host: return None

        widget = manager.instance(host)
        if not widget: return None

        window.setCentralWidget(widget)
        widget.back.connect(functools.partial(self.onActionDashboard, window=window))


    @inject.params(manager='manager_device')
    def onActionHostOpen(self, host, manager, window):
        if not host: return None

        widget = manager.instance(host)
        if not widget: return None

        window.setCentralWidget(widget)
        widget.back.connect(functools.partial(self.onActionDashboard, window=window))
