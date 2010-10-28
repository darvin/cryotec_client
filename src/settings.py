# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from qtdjango.connection import *

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

    def __init__(self, parent=None, error_message=None):
        self.__widgets = (
#            (name, caption, widget object, default value),
            ("address", u"Адрес сервера", QLineEdit(), "http://127.0.0.1:8000"),
            ("api_path", u"Путь к api сервера", QLineEdit(), "/api/"),
            ("server_package", u"Название пакета сервера", QLineEdit(), "cryotec_server"),
            ("login", u"Ваш логин", QLineEdit(), ""),
            ("password", u"Ваш пароль", QLineEdit(), ""),

            ("applicationStyle", u"Стиль приложения", StyleComboBox(), "windowsxp"),
        )
        super(SettingsDialog, self).__init__(parent)
        self.setModal(True)
        self.formlayout = QFormLayout()
        self.settings = QSettings()
        self.message_widget = QLabel()
        for name, caption, widget, default in self.__widgets:
            self.formlayout.addRow(caption, widget)
            widget.setText(self.settings.value(name, default).toString())

        self.formlayout.addRow(self.message_widget)

        if error_message is not None:
            self.message(**error_message)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Save\
            | QDialogButtonBox.Cancel |QDialogButtonBox.RestoreDefaults)

        testButton = QPushButton(u"Тестировать соединение")
        buttonBox.addButton(testButton, QDialogButtonBox.ActionRole)
        testButton.clicked.connect(self.test)
        resetButton = QPushButton(u"Сбросить настройки")
        buttonBox.addButton(resetButton, QDialogButtonBox.DestructiveRole)
        resetButton.clicked.connect(self.reset)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore)
        self.formlayout.addRow(buttonBox)
        self.setLayout(self.formlayout)

    def accept(self):
        if self.test():
            for name, caption, widget, default in self.__widgets:
                self.settings.setValue(name, widget.text())
            QDialog.accept(self)

    def restore(self):
        for name, caption, widget, default in self.__widgets:
            widget.setText(default)

    def message(self, text, error=False, works=False, fields=[]):
        self.message_widget.setText(text)
        if error:
            color = "red"
        elif works:
            color = "green"
        else:
            color = "black"

        css = "QLabel { color : %s; }" % color
        self.message_widget.setStyleSheet(css)
        for name, caption, widget, default in self.__widgets:
            self.formlayout.labelForField(widget).setStyleSheet("")
            if name in fields:
                self.formlayout.labelForField(widget).setStyleSheet(css)



    def test(self):
        s = {}
        for name, caption, widget, default in self.__widgets:
            s[name] = unicode(widget.text())

        c = Connection(s["address"],s["api_path"],s["login"],s["password"])


        remote_version = None
        try:
            remote_version = c.get_resource_from_server("info")["qtdjango_version"]
            import qtdjango
            if qtdjango.__version__==remote_version:
                self.message(text=u"Удаленный сервер настроен правильно!", works=True)
                return True
            elif remote_version is not None:
                self.message(u"Версия системы на удаленном сервере отличается от\
версии системы на клиенте")
                return True

        except SocketError:
            self.message(text=u"Ошибка при подключении к удаленному серверу", error=True, fields=\
                            ("address",))
        except ServerNotFoundError:
            self.message(text=u"Удаленный сервер недоступен", error=True, fields=\
                            ("address",))
        except NotQtDjangoResponceError:
            self.message(text=u"Не правильно настроен путь на удаленном сервере или \
удаленный сервер не является сервером системы", error=True, fields=\
                            ("address","api_path"))


        return False




    def reset(self):
        print "reset"


def check_settings(parent):

    settings = QSettings()

    while not settings.contains("address"):
        print "settings dialog"
        sd = SettingsDialog(parent=parent)
        sd.exec_()


def error_settings(parent, message):
    sd = SettingsDialog(parent=parent, error_message=message)
    sd.exec_()

def get_settings(name):
    settings = QSettings()
    return unicode(settings.value(name).toString())

