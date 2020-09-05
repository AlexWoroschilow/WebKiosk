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
import base64

import inject
import requests


class ApiClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @property
    @inject.params(config='config')
    def headers(self, config):
        return {"token": config.get('security.code')}

    @inject.params(config='config')
    def url(self, page, config):

        try:
            url = 'http://{}:{}/api/page/open'.format(self.host, self.port)
            response = requests.post(url, json={"url": page}, headers=self.headers).json()
        except Exception as ex:
            return None

        if 'screenshot' in response.keys():
            response['screenshot']['picture'] = base64.b64decode(
                response.get('screenshot').get('picture')
            )

        return response

    @inject.params(config='config')
    def status(self, config):
        try:
            url = 'http://{}:{}/api/status'.format(self.host, self.port)
            response = requests.get(url, headers=self.headers).json()
        except Exception as ex:
            return None

        if 'screenshot' in response.keys():
            response['screenshot']['picture'] = base64.b64decode(
                response.get('screenshot').get('picture')
            )

        return response

    @inject.params(config='config')
    def ping(self, config):

        try:
            url = 'http://{}:{}/api/ping'.format(self.host, self.port)
            return requests.get(url, headers=self.headers).json()
        except Exception as ex:
            return None

    @inject.params(config='config')
    def screenshot(self, config=None):

        try:
            url = 'http://{}:{}/api/screenshot'.format(self.host, self.port)
            response = requests.get(url, headers=self.headers)
            response = response.json()
        except Exception as ex:
            return None

        if 'picture' not in response.keys():
            return None

        try:
            return base64.b64decode(response['picture'])
        except Exception as ex:
            print(ex)
            return None


class ApiClientManager(object):
    def __init__(self, config):
        pass

    def instance(self, host, port):
        return ApiClient(host, port)
