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


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options, args):
        return not hasattr(options, 'server')

    def configure(self, binder, options, args):
        binder.bind_to_provider('manager_scanner', self.__scanner)

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
