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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class LabelTitle(QtWidgets.QLabel):

    def __init__(self, name):
        super(LabelTitle, self).__init__(name)
        self.setStyleSheet("QLabel { font-size: 22px; }")
        self.setAlignment(Qt.AlignCenter)


class LabelSubtitle(QtWidgets.QLabel):

    def __init__(self, name):
        super(LabelSubtitle, self).__init__(name)
        self.setStyleSheet("QLabel { font-size: 18px; }")
        self.setAlignment(Qt.AlignCenter)


class LabelText(QtWidgets.QLabel):

    def __init__(self, name):
        super(LabelText, self).__init__(name)
        self.setStyleSheet("QLabel { font-size: 12px; }")
        self.setAlignment(Qt.AlignCenter)
