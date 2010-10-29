# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from qtdjango.connection import *

__author__ = 'darvin'


from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qtdjango.settings


class StyleComboBox(QComboBox):
    styles = QStyleFactory.keys()
    def __init__(self, *args, **kwargs):
        super(StyleComboBox,self).__init__(*args, **kwargs)
        self.addItems(self.styles)
        self.currentIndexChanged.connect(self.change_style)

    def setText(self, str):
        self.setCurrentIndex(self.findText(str))

    @QtCore.pyqtSlot(int)
    def change_style(self, style_num):
        style = self.itemText(style_num)
        app = qApp
        app.setStyle(style)

    def text(self):
        return self.currentText()


class SettingsDialog(qtdjango.settings.SettingsDialog):
    widgets_table = qtdjango.settings.SettingsDialog.widgets_table +\
            [("applicationStyle", u"Стиль приложения", StyleComboBox, "windowsxp"),]
    def __init__(self, *args, **kwargs):
        super(SettingsDialog,self).__init__(*args, **kwargs)


def check_settings(parent):

    settings = QSettings()

    while not settings.contains("address"):
        print "settings dialog"
        sd = SettingsDialog(parent=parent)
        sd.exec_()



def get_settings(name):
    settings = QSettings()
    return unicode(settings.value(name).toString())

