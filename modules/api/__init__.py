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

    def configure(self, binder, options, args):
        binder.bind_to_constructor('api.controller', self.__api_service)
        binder.bind_to_constructor('api.client_manager', self.__client_manager)

    @inject.params(config='config')
    def __api_service(self, config):
        from modules.api.server import controller
        return controller

    @inject.params(config='config')
    def __client_manager(self, config):
        from modules.api.client import ApiClientManager
        return ApiClientManager(config)
