# -*- coding: utf-8 -*-


from PyQt4.QtGui import QDockWidget
from PyQt4 import QtCore
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

    def show_responce(self, responces):
        """
        Shows responce from server
        @param responces: dict responce from server
        """
        html = u""
        total_errors = 0
        for model_name, model_resp in responces.items():
            if model_resp:
                html +=u"<h1>%s</h1>" % (model_name,)
                success = 0
                errors = 0
                for inst_resp in model_resp:
                    from pprint import pprint
                    pprint(inst_resp)
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


