# Copyright 2020 Alex Woroschilow (alex@ergofox.me)
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
PWD:=$(shell pwd)
SHELL := $(shell which bash)
APPDIR_SERVER := ./Server.AppDir
APPDIR_CONSOLE := ./Console.AppDir
PYTHON := python3.8

all: latest rpm


appdir: clean
	rm -rf $(PWD)/build
	mkdir -p $(PWD)/build
	mkdir -p $(PWD)/build/AppDir

	wget --output-document=$(PWD)/build/build.rpm  http://ftp.altlinux.org/pub/distributions/ALTLinux/Sisyphus/armh/RPMS.classic/python3-3.8.5-alt1.armh.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://ftp.altlinux.org/pub/distributions/ALTLinux/Sisyphus/armh/RPMS.classic/libpython3-3.8.5-alt1.armh.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://ftp.altlinux.org/pub/distributions/ALTLinux/Sisyphus/armh/RPMS.classic/python3-module-PyQtWebEngine-5.13.1-alt3.armh.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://ftp.altlinux.org/pub/distributions/ALTLinux/Sisyphus/armh/RPMS.classic/python3-module-PyQt5-sip-4.19.19-alt3.armh.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://ftp.altlinux.org/pub/distributions/ALTLinux/Sisyphus/armh/RPMS.classic/python3-module-Cython-0.29.21-alt1.armh.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://ftp.altlinux.org/pub/distributions/ALTLinux/Sisyphus/armh/RPMS.classic/python3-module-PyQt5-5.13.1-alt2.armh.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	wget --output-document=$(PWD)/build/build.rpm  http://ftp.altlinux.org/pub/distributions/ALTLinux/Sisyphus/armh/RPMS.classic/libffi7-3.3-alt1.armh.rpm
	cd $(PWD)/build && rpm2cpio $(PWD)/build/build.rpm | cpio -idmv && cd ..

	mkdir -p $(PWD)/build/AppDir/python
	cp -r $(PWD)/build/usr/* $(PWD)/build/AppDir/python

	cp --force $(PWD)/AppDir/AppRun $(PWD)/build/AppDir/AppRun
	chmod +x $(PWD)/build/AppDir/AppRun


clean:
	rm -rf ${PWD}/build
