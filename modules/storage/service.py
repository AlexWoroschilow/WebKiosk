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
import logging

import inject
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from .schema.ergoscan import BaseCustom
from .schema.ergoscan import Host
from .schema.ergoscan import HostFound


class Storage(object):
    _engine = None
    _session = None

    @inject.params(config='config')
    def __init__(self, config=None):

        self._engine = create_engine('sqlite:///{}'.format(config.get('storage.database')), poolclass=NullPool)

        session = self.session_instance
        if session is None:
            return None

        BaseCustom.query = session.query_property()
        BaseCustom.metadata.create_all(bind=self._engine)

        session.commit()

    @property
    def session_instance(self):
        if self._session is not None:
            return self._session

        self._session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        ))

        return self.session_instance


class ServiceStorage(Storage):

    @property
    def scanned(self):
        session = self.session_instance
        if session is not None:
            return session.query(HostFound).all()
        return []

    @property
    def hosts(self):
        session = self.session_instance
        if session is not None:
            return session.query(Host).all()
        return []

    def append(self, entity):
        session = self.session_instance
        if not session: return None

        try:
            session.add(entity)
            session.commit()
        except(InvalidRequestError, Exception) as ex:
            logging.getLogger('database').exception(ex)
            session.rollback()
            session.close()

        return entity

    def update(self, entity):
        session = self.session_instance
        if session is not None:
            session.commit()
        return entity

    def getHostFoundByIp(self, ip):
        session = self.session_instance
        if session is not None:
            return session.query(HostFound) \
                .filter(HostFound.ip == ip) \
                .one_or_none()
        return None

    def found(self, entity=None):
        (ip, screenshot) = entity
        session = self.session_instance
        if not session: return None

        entity = HostFound(ip=ip, name=ip, screenshot=screenshot)

        try:
            session.add(entity)
            session.commit()
            return entity
        except(InvalidRequestError, Exception) as ex:
            logging.getLogger('database').exception(ex)
            session.rollback()
            session.close()

        return None

    def remove(self, entity=None):
        session = self.session_instance
        if not session: return None

        try:
            session.delete(entity)
            session.commit()
        except(InvalidRequestError, Exception) as ex:
            logging.getLogger('database').exception(ex)
            session.rollback()
            session.close()

        return None

    def save(self, found=None):
        session = self.session_instance
        if not session: return None

        entity = Host(ip=found.ip, name=found.ip, screenshot=found.screenshot)

        try:
            session.add(entity)
            session.commit()
            return entity
        except(InvalidRequestError, Exception) as ex:
            logging.getLogger('database').exception(ex)
            session.rollback()
            session.close()

        return None
