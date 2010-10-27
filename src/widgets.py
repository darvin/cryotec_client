# -*- coding: utf-8 -*-

from PyQt4.QtWebKit import QWebView
#noinspection PyUnresolvedReferences
import PyQt4.QtNetwork
from PyQt4.QtGui import QDockWidget, QTreeWidget
from PyQt4 import QtCore
from qtdjango.models import Model

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
        self.webview = QWebView()
        self.setWidget(self.webview)
        self.webview.setHtml("")

    @QtCore.pyqtSlot(Model)
    def modelChanged(self, model):
        header1 = model.__class__.verbose_name()
        header2 = "" #unicode(model)
        fields = model.__class__.get_fields()
        field_text_values = {}
        for fieldname, field in fields.items():
            if not fieldname in ("user", "id", "extra_to_html"):
                field_text_values[fieldname] = []
                field_text_values[fieldname].append(field.verbose_name)
                field_text_values[fieldname].append(field.to_text(getattr(model, fieldname)))


        html = u""
        html += u"<h1>%s</h1><h2>%s</h2>" %(header1,header2)
        html += u"<br>".join([u"<b>%s:</b> <i>%s</i>"%(x[0], x[1]) for x in field_text_values.values()])

        try:
            html += "<br>" + model.extra_to_html
        except AttributeError:
            pass
        except TypeError:
            pass

        self.webview.setHtml(html)
        print self.webview.page().mainFrame().contentsSize()

    @QtCore.pyqtSlot()
    def modelCleared(self):
        self.webview.setHtml("")


