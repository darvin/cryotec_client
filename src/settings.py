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
    widgets_table = [
                    ("address", u"Адрес сервера", QLineEdit, "http://cryotec.webfactional.com"),
                    ("api_path", u"Путь к api сервера", QLineEdit, "/api/"),
                    ("server_package", u"Название пакета сервера", QLineEdit, "cryotec_server"),
                    ("login", u"Ваш логин", QLineEdit, ""),
                    ("password", u"Ваш пароль", QLineEdit, ""),
                    ("open_links_in_external_browser", \
                        u"Открывать ссылки из окна информации во внешнем браузере", qtdjango.settings.BooleanEdit, True),
                    ("applicationStyle", u"Стиль приложения", StyleComboBox, "Plastique"),]
    def __init__(self, *args, **kwargs):
        super(SettingsDialog,self).__init__(*args, **kwargs)


def setup_settings():

    settings = QSettings()

    if not (settings.contains("address") or settings.contains("server_package")):
        for name, caption, widget_class, default in SettingsDialog.widgets_table:
            settings.setValue(name, default)







def get_settings(name):
    settings = QSettings()
    return unicode(settings.value(name).toString())

