# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from settings import SettingsDialog

__author__ = 'darvin'

class ConnectionErrorDialog(QDialog):
    def __init__(self, parent=None, message=None, models_manager=None, *args, **kwargs):
        super(ConnectionErrorDialog,self).__init__(parent, *args, **kwargs)
        self.message, self.models_manager = message, models_manager
        self.label = QLabel(u"Не могу подключиться к серверу\n"+self.message["text"])
        layout = QVBoxLayout()
        fileButton = QPushButton(u"Загрузить состояние из файла")
        settingsButton = QPushButton(u"Изменить настройки")

        buttonbox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonbox.rejected.connect(self.reject)
        buttonbox.addButton(settingsButton, QDialogButtonBox.AcceptRole)
        settingsButton.clicked.connect(self.settings_clicked)
        buttonbox.addButton(fileButton, QDialogButtonBox.AcceptRole)
        fileButton.clicked.connect(self.file_clicked)
        layout.addWidget(self.label)
        layout.addWidget(buttonbox)
        self.setLayout(layout)

    def settings_clicked(self):
        sd = SettingsDialog(parent=self.parent(), error_message=self.message,\
                    models_manager=self.models_manager)
        if sd.exec_()==QDialog.Accepted:
            self.accept()

    def file_clicked(self):
        fileName = QFileDialog.getOpenFileName(self, u"Открыть состояние",\
                filter=u"Файлы состояний (*.crs)")

        f = open(fileName,'r')

        if self.models_manager.load_from_file(f):
            self.accept()

