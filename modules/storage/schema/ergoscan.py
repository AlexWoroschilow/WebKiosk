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
from sqlalchemy import Column 
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import BLOB
from sqlalchemy import Integer
from sqlalchemy import DateTime

from sqlalchemy.ext.declarative import declarative_base

BaseCustom = declarative_base()


class HostFound(BaseCustom):
    __tablename__ = 'HostsFound'
    id = Column(Integer, primary_key=True)
    createdAt = Column(DateTime)
    ip = Column(String(255))
    name = Column(String(255))
    description = Column(Text)
    ports = Column(Text)
    services = Column(Text)

    screenshot = Column(BLOB)


class Host(BaseCustom):
    __tablename__ = 'Hosts'
    id = Column(Integer, primary_key=True)
    createdAt = Column(DateTime)
    ip = Column(String(255))
    name = Column(String(255))
    description = Column(Text)
    ports = Column(Text)
    services = Column(Text)
    screenshot = Column(BLOB)

    def __eq__(self, a):
        return self.ip == a.ip 
        
