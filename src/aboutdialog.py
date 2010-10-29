# -*- coding: utf-8 -*-
from PyQt4.QtGui import *

__author__ = 'darvin'
#FIXME!!!
import __init__

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog,self).__init__(*args, **kwargs)
        self.label = QLabel()
        layout = QVBoxLayout()
        #FIXME!!!
        html = u"""Программа-клиент для системы журналирования неисправностей оборудования.<br>
Версия %s
""" % __init__.__version__
        self.label.setText(html)
        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonbox.accepted.connect(self.accept)
        layout.addWidget(self.label)
        layout.addWidget(buttonbox)
        self.setLayout(layout)