# -*- coding: utf-8 -*-

'''
@author: darvin
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from settings import check_settings, error_settings, SettingsDialog
import images_rc, translation_rc
from widgets import ServerResponceDock, ShowModelInfoDock
from aboutdialog import AboutDialog
import settings

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1024,768)
        from views import FixWithButtonsView, ReportWithButtonsView, \
                MaintenanceWithButtonsView, CheckupWithButtonsView, MachinePanel

        from models import models
        self.machine_tree = MachinePanel()


        self.info_dock = ShowModelInfoDock(u"Информация", self)
        self.info_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea |\
                                Qt.BottomDockWidgetArea)

        self.machine_tree.view.modelSelectionChanged.connect(self.info_dock.modelChanged)
        self.machine_tree.view.modelSelectionCleared.connect(self.info_dock.modelCleared)



        self.note_views = {
                u"Неисправности":ReportWithButtonsView(None),
                u"Ремонты":FixWithButtonsView(None),
                u"Техобслуживания":MaintenanceWithButtonsView(None),
                u"Контроли моточасов":CheckupWithButtonsView(None),
                }
        #self.machine_tree.setSelectionMode(QAbstractItemView.MultiSelection)
        self.notebook = CentralNotebook(self.machine_tree, self.info_dock, self.note_views)

        self.setCentralWidget(self.notebook)

        machineDockWidget = QDockWidget(u"Оборудование", self)
        machineDockWidget.setObjectName("machine_dock")

        machineDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        machineDockWidget.setWidget(self.machine_tree)


        self.responce_dock = ServerResponceDock(u"Ответ от сервера", self)
        self.responce_dock.setAllowedAreas(Qt.RightDockWidgetArea|Qt.BottomDockWidgetArea)


        self.settings_dialog = SettingsDialog()
        settingsAction = QAction(QIcon(":/icons/setting_tools.png"), u"Настройки", self)
        settingsAction.triggered.connect(self.settings_dialog.exec_)

        self.about_dialog = AboutDialog(self)
        aboutAction = QAction(u"О программе...", self)
        aboutAction.triggered.connect(self.about_dialog.exec_)



        self.syncAction = QAction(QIcon(":/icons/update.png"), u"Синхронизировать", self)
        self.syncAction.triggered.connect(self.synchronize)
        syncButton = QToolButton()
        syncButton.setDefaultAction(self.syncAction)
        syncButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        syncStatusBarButton = QToolButton()
        syncStatusBarButton.setDefaultAction(self.syncAction)
        self.syncProgress = QProgressBar()
        self.syncProgress.setRange(0,0)
        self.syncProgress.setVisible(False)
        self.syncProgress.setTextVisible(False)
        self.syncProgress.setMinimumSize(QSize(2,2))
        self.syncProgress.setMaximumSize(QSize(40,20))



        machinetreepanelAction = machineDockWidget.toggleViewAction()
        machinetreepanelAction.setIcon(QIcon(":/icons/application_side_tree.png"))

        responcedockAction = self.responce_dock.toggleViewAction()

        infodockAction = self.info_dock.toggleViewAction()

        self.statusBar().showMessage(u'Информация с сервера загружена')

        self.statusBar().addPermanentWidget(self.syncProgress)
        self.statusBar().addPermanentWidget(syncStatusBarButton)

        quitAction = QAction(u"Выход", self)
        quitAction.triggered.connect(self.close)


        self.mm = models
        self.mm.add_notify_dumped(self.synced)
        self.mm.add_notify_undumped(self.unsynced)



        self.addDockWidget(Qt.LeftDockWidgetArea, machineDockWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.info_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.responce_dock)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)


        mainmenu = self.menuBar()
        filemenu = mainmenu.addMenu(u"Файл")
        viewmenu = mainmenu.addMenu(u"Вид")
        connmenu = mainmenu.addMenu(u"Соединение")
        helpmenu = mainmenu.addMenu(u"Справка")

        viewmenu.addAction(machinetreepanelAction)
        viewmenu.addAction(responcedockAction)
        viewmenu.addAction(infodockAction)
        connmenu.addAction(self.syncAction)
        filemenu.addAction(settingsAction)
        filemenu.addAction(quitAction)
        helpmenu.addAction(aboutAction)

        toolbar = self.addToolBar("main")
        toolbar.setObjectName("main_toolbar")
        toolbar.addAction(machinetreepanelAction)
        toolbar.addWidget(syncButton)
        toolbar.addAction(settingsAction)

        settings = QSettings()
        self.restoreGeometry(settings.value("geometry").toByteArray());
        self.restoreState(settings.value("windowState").toByteArray());
        for widget in self.note_views.values():
            table_name = widget.view.__class__.__name__+"State"
            widget.view.horizontalHeader().restoreState(settings.value(table_name, "").toByteArray())

    def synchronize(self):
        """Synchronizes ModelsManager"""
        self.syncProgress.setVisible(True)
        qApp.processEvents()
        self.mm.dump()

    def synced(self, responces):
        self.statusBar().showMessage(u'Синхронизированно')
        self.syncAction.setIcon(QIcon(":/icons/update.png"))

        self.syncProgress.setVisible(False)
#        self.syncProgress.hide()

        self.responce_dock.show_responce(responces)
        qApp.processEvents()

    def unsynced(self):
        self.statusBar().showMessage(u'Есть несохранненные записи')
        self.syncAction.setIcon(QIcon(":/icons/unupdated.png"))


    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        for widget in self.note_views.values():
            table_name = widget.view.__class__.__name__+"State"
            settings.setValue(table_name, widget.view.horizontalHeader().saveState())

        QMainWindow.closeEvent(self, event)


class CentralNotebook(QTabWidget):
    def __init__(self, machine_tree, info_dock, views, parent=None):
        super(CentralNotebook, self).__init__(parent)
        self.widgets = []
        self.machine_tree, self.info_dock = machine_tree, info_dock
        for label, widget in views.items():
            w = widget
            machine_tree.view.modelSelectionChanged.connect(w.filterModelSelected)
            w.view.modelSelectionChanged.connect(self.info_dock.modelChanged)
            machine_tree.view.modelSelectionCleared.connect(w.filterCleared)

            self.widgets.append(w)
            self.addTab(w, label)


import sys

def main():
    app = QApplication(sys.argv)  # создаёт основной объект программы
    app.setApplicationName("CryotecClient")
    app.setOrganizationName("SKOpenCodes")
    app.setOrganizationDomain("skopencodes.org")


    qtTranslator = QTranslator()
    if qtTranslator.load("qt",":/"):
        app.installTranslator(qtTranslator)

    appTranslator = QTranslator()
    if appTranslator.load("cryotec_client", ":/"):
        app.installTranslator(appTranslator)


    settings = QSettings()
    app.setStyle(settings.value("applicationStyle", "windowsxp").toString())
    pixmap = QPixmap(":/images/splashscreen.png")
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.setMask(pixmap.mask()) # this is usefull if the splashscreen is not a regular ractangle...
    splash.show()
    splash.showMessage((u'Криотек Клиент'), Qt.AlignRight | Qt.AlignBottom,
    Qt.white)
    # make sure Qt really display the splash screen
    app.processEvents()
    check_settings(splash)

    try:
        from models import models
    except ImportError:
        error_settings(splash, {"fields":("server_package"),
                                "text":u"Проверьте название пакета сервера",
                                "error":True})

    except:
        error_settings(splash, {"fields":("address","api_path"),
                                "text":u"Проверьте настройки сервера",
                                "error":True})

    form = MainWindow()  # создаёт объект формы
    splash.finish(form)
    form.show()  # даёт команду на отображение объекта формы и содержимого
    app.exec_()  # запускает приложение

if __name__ == "__main__":
    sys.exit(main()) 
