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
import socket
import time
from builtins import int

import inject
import netifaces
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask
from flask_restplus import Api, Resource

controller = Flask('WebKiosk')
api = Api(controller)


class WebKioskResource(Resource):

    @property
    def ip(self):
        addresses = []
        for iface in netifaces.interfaces():
            for data in netifaces.ifaddresses(iface).setdefault(netifaces.AF_INET, [{'addr': None}]):
                if data['addr'] not in [None, '127.0.0.1']:
                    addresses.append(data['addr'])
        return addresses

    @property
    def network(self):
        response = []
        for iface in netifaces.interfaces():
            addresses = []
            for data in netifaces.ifaddresses(iface).setdefault(netifaces.AF_INET, [{'addr': None}]):
                addresses.append(data['addr'])
            response.append({
                'name': iface,
                'ip': addresses
            })
        return response


@api.route('/api/ping')
class Ping(WebKioskResource):
    parser = api.parser()
    parser.add_argument('token', required=True, help="Authentication token", location='headers')

    @inject.params(config='config')
    @api.expect(parser)
    def get(self, config):
        args = self.parser.parse_args()
        if args['token'] != config.get('security.code'):
            return {'error': 'Unknown client'}

        return {
            'host': socket.gethostname(),
            'network': self.network,
            'ip': self.ip
        }


@api.route('/api/screenshot')
class Screenshot(WebKioskResource):
    parser = api.parser()
    parser.add_argument('token', required=True, help="Authentication token", location='headers')

    @inject.params(config='config', browser='browser')
    @api.expect(parser)
    def get(self, config, browser):
        args = self.parser.parse_args()
        if args['token'] != config.get('security.code'):
            return {'error': 'Unknown client'}

        browser.screenshotAction.emit(self)

        screenshot = browser.get_screenshot_latest()
        screenshot = base64.b64encode(screenshot)

        return {
            'picture': screenshot.decode('utf-8'),
            'timestamp': int(time.time()),
        }


@api.route('/api/status')
class Status(WebKioskResource):
    parser = api.parser()
    parser.add_argument('token', required=True, help="Authentication token", location='headers')

    @inject.params(config='config', browser='browser')
    @api.expect(parser)
    def get(self, config, browser):
        args = self.parser.parse_args()
        if args['token'] != config.get('security.code'):
            return {'error': 'Unknown client'}

        browser.screenshotAction.emit(self)

        screenshot = browser.get_screenshot_latest()
        screenshot = base64.b64encode(screenshot)

        return {
            'screenshot': {
                'picture': screenshot.decode('utf-8'),
                'timestamp': int(time.time()),
            },
            'url': config.get('browser.url'),
            'timestamp': int(time.time()),
            'host': socket.gethostname(),
            'network': self.network,
            'ip': self.ip
        }


@api.route('/api/page/open')
class Page(WebKioskResource):
    parser = api.parser()
    parser.add_argument('token', required=True, help="Authentication token", location='headers')
    parser.add_argument('url', required=True, help="Please specify url", location='json')

    @inject.params(config='config', browser='browser')
    @api.expect(parser)
    def post(self, config, browser):
        args = self.parser.parse_args()
        if args['token'] != config.get('security.code'):
            return {'error': 'Unknown client'}

        config.set('browser.url', args['url'])

        browser.pageAction.emit(args)

        browser.screenshotAction.emit(self)

        screenshot = browser.get_screenshot_latest()
        screenshot = base64.b64encode(screenshot)

        return {
            'picture': screenshot.decode('utf-8'),
            'timestamp': int(time.time()),
        }
