# -*- coding: utf-8 -*-
from PyQt4 import QtCore

__author__ = 'darvin'


from PyQt4.QtCore import *
from PyQt4.QtGui import *


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


class SettingsDialog(QDialog):
    __error_messages = {
        "server_package": u"Название пакета сервера введено неверно.",
        "address": u"Адрес сервера введен неверно",
        "api_path": u"URL путь недоступен",
    }

    def __init__(self, parent=None, error_setting=None):
        self.__widgets = (
#            (name, caption, widget object, default value),
            ("address", u"Адрес сервера", QLineEdit(), "http://127.0.0.1:8000"),
            ("api_path", u"Путь к api сервера", QLineEdit(), "/api/"),
            ("server_package", u"Название пакета сервера", QLineEdit(), "cryotec_server"),
            ("applicationStyle", u"Стиль приложения", StyleComboBox(), "windowsxp"),
        )
        super(SettingsDialog, self).__init__(parent)
        self.setModal(True)
        self.formlayout = QFormLayout()
        self.settings = QSettings()
        for name, caption, widget, default in self.__widgets:
            if error_setting==name:
                caption = "<b>"+caption+"</b>"
            self.formlayout.addRow(caption, widget)
            widget.setText(self.settings.value(name, default).toString())
        if error_setting is not None:
            self.formlayout.addRow(QLabel(self.__error_messages[error_setting]))

        buttonBox = QDialogButtonBox(QDialogButtonBox.Save\
            | QDialogButtonBox.Cancel |QDialogButtonBox.RestoreDefaults)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore)
        self.formlayout.addRow(buttonBox)
        self.setLayout(self.formlayout)

    def accept(self):
        for name, caption, widget, default in self.__widgets:
            self.settings.setValue(name, widget.text())
        QDialog.accept(self)

    def restore(self):
        for name, caption, widget, default in self.__widgets:
            widget.setText(default)


def check_settings(parent):

    settings = QSettings()

    while not settings.contains("address"):
        print "settings dialog"
        sd = SettingsDialog(parent=parent)
        sd.exec_()


def error_settings(parent, name):
    settings = QSettings()
    old_setting = settings.value(name)
    while settings.value(name)==old_setting:
        print "error settings"
        sd = SettingsDialog(parent=parent, error_setting=name)
	sd.show()
        sd.exec_()

def get_settings(name):
    settings = QSettings()
    return unicode(settings.value(name).toString())

