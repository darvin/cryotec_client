# -*- coding: utf-8 -*-


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qtdjango.models import Model
from views import InfoView

#noinspection PyUnresolvedReferences
import PyQt4.QtNetwork
from PyQt4.QtWebKit import QWebView

__author__ = 'darvin'

class ServerResponceDock(QDockWidget):
    def __init__(self, *args, **kwargs):
        super(ServerResponceDock,self).__init__(*args, **kwargs)
        self.setObjectName("responce_dock")
        self.webview = QWebView()
        self.setWidget(self.webview)
        self.webview.setHtml("")
        self.hide()

    def show_responce(self, responces=None):
        """
        Shows responce from server
        @param responces: dict responce from server
        """
        html = u""
        total_errors = 0
        if responces is not None:
            for model_name, model_resp in responces.items():
                if model_resp:
                    html +=u"<h1>%s</h1>" % (model_name,)
                    success = 0
                    errors = 0
                    for inst_resp in model_resp:
                        if inst_resp["headers"]["status"]=="200":
                            success += 1
                        else:
                            html += inst_resp["body"]
                            if inst_resp["headers"]["status"]=="500":
                                html = u"<pre>%s</pre>" % (html,)
                            errors += 1
                    html += u"%d объектов успешно добавлено.<br>"%(success,)
                    if errors:
                        html += u"%d ошибок<br>"%(errors,)
                    total_errors += errors


        self.webview.setHtml(html)
        if total_errors:
            self.show()


class ShowModelInfoDock(QDockWidget):
    def __init__(self, *args, **kwargs):
        super(ShowModelInfoDock,self).__init__(*args, **kwargs)
        self.setObjectName("info_dock")
        self.view = InfoView()
        self.setWidget(self.view)


class StatusBar(QStatusBar):

    clicked = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super(StatusBar,self).__init__(*args, **kwargs)


        self.syncProgress = QProgressBar()
        self.syncProgress.setRange(0,0)
        self.syncProgress.setVisible(False)
        self.syncProgress.setTextVisible(False)
        self.syncProgress.setMinimumSize(QSize(2,2))
        self.syncProgress.setMaximumSize(QSize(40,20))
        self.addPermanentWidget(self.syncProgress)

        self.userLabel = QLabel(u"<font color=red>Пользователь не установлен</font>")


        self.addPermanentWidget(self.userLabel)
        self.syncPixmap = QLabel()
        self.addPermanentWidget(self.syncPixmap)




    def synced(self, responces=None):
        self.showMessage(u'Синхронизированно')
        self.syncPixmap.setPixmap(QPixmap(":/small_icons/update.png"))

        self.syncProgress.setVisible(False)
#        self.syncProgress.hide()

        qApp.processEvents()


    def unsynced(self):

        self.syncPixmap.setPixmap(QPixmap(":/small_icons/unupdated.png"))
        self.showMessage(u'Есть несохранненные записи')

    def synchronize(self):
        """Synchronizes ModelsManager"""
        self.syncProgress.setVisible(True)
        qApp.processEvents()

    @pyqtSlot(Model)
    def userChanged(self, user):
        self.userLabel.setText(u"<b>%s</b>" % unicode(user))


    def mousePressEvent(self, event):
        self.clicked.emit()