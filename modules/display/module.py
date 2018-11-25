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
import Xlib.display

from lib.plugin import Loader


class Loader(Loader):

    @property
    def enabled(self):
        if hasattr(self._options, 'server'):
            return self._options.server
        return False

    def config(self, binder=None):

        display = Xlib.display.Display()
        if display is None or not display:
            return None
        
        display_current = display.screen().root
        if display_current is None or not display_current:
            return None

        binder.bind('display', display_current.get_geometry())
 
