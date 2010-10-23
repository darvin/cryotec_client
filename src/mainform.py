# -*- coding: utf-8 -*-

'''
@author: darvin
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from settings import check_settings, SettingsDialog
import images_rc

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1024,768)
        from views import FixWithButtonsView, ReportWithButtonsView, \
                MaintenanceWithButtonsView, CheckupWithButtonsView, MachinePanel
        from models import models


        self.machine_tree = MachinePanel()
        self.note_views = {
                u"Неисправности":ReportWithButtonsView(None),
                u"Ремонты":FixWithButtonsView(None),
                u"Техобслуживания":MaintenanceWithButtonsView(None),
                u"Контроли моточасов":CheckupWithButtonsView(None),
                }
        #self.machine_tree.setSelectionMode(QAbstractItemView.MultiSelection)
        self.notebook = CentralNotebook(self.machine_tree, self.note_views)

        self.setCentralWidget(self.notebook)

        dockWidget = QDockWidget(u"Оборудование", self)

        dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dockWidget.setWidget(self.machine_tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)


        self.settings_dialog = SettingsDialog()
        settingsAction = QAction(QIcon(":/icons/setting_tools.png"), u"Настройки", self)
        settingsAction.triggered.connect(self.settings_dialog.exec_)


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



        machinetreepanelAction = dockWidget.toggleViewAction()
        machinetreepanelAction.setIcon(QIcon(":/icons/application_side_tree.png"))
        toolbar = self.addToolBar("main")

        toolbar.addAction(machinetreepanelAction)
        toolbar.addWidget(syncButton)
        toolbar.addAction(settingsAction)


        self.statusBar().showMessage(u'Информация с сервера загружена')

        self.statusBar().addPermanentWidget(self.syncProgress)
        self.statusBar().addPermanentWidget(syncStatusBarButton)




        self.mm = models
        self.mm.add_notify_dumped(self.synced)
        self.mm.add_notify_undumped(self.unsynced)


    def synchronize(self):
        """Synchronizes ModelsManager"""
        self.syncProgress.setVisible(True)
        qApp.processEvents()
        self.mm.dump()

    def synced(self):
        self.statusBar().showMessage(u'Синхронизированно')
        self.syncAction.setIcon(QIcon(":/icons/update.png"))

        self.syncProgress.setVisible(False)
#        self.syncProgress.hide()
        qApp.processEvents()

    def unsynced(self):
        self.statusBar().showMessage(u'Есть несохранненные записи')
        self.syncAction.setIcon(QIcon(":/icons/unupdated.png"))





class CentralNotebook(QTabWidget):
    def __init__(self, machine_tree, views, parent=None):
        super(CentralNotebook, self).__init__(parent)
        self.widgets = []
        self.machine_tree = machine_tree
        for label, widget in views.items():
            w = widget
            machine_tree.view.modelSelectionChanged.connect(w.filterByMachine)
            machine_tree.view.modelSelectionCleared.connect(w.filterCleared)

            self.widgets.append(w)
            self.addTab(w, label)


import sys

def main():
    app = QApplication(sys.argv)  # создаёт основной объект программы
    app.setApplicationName("CryotecClient")
    app.setOrganizationName("SKOpenCodes")
    app.setOrganizationDomain("skopencodes.org")
    pixmap = QPixmap(":/images/splashscreen.png")
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.setMask(pixmap.mask()) # this is usefull if the splashscreen is not a regular ractangle...
    splash.show()
    splash.showMessage((u'Криотек Клиент'), Qt.AlignRight | Qt.AlignBottom,
    Qt.white)
    # make sure Qt really display the splash screen
    app.processEvents()
    check_settings()
    form = MainWindow()  # создаёт объект формы
    splash.finish(form)
    form.show()  # даёт команду на отображение объекта формы и содержимого
    app.exec_()  # запускает приложение

if __name__ == "__main__":
    sys.exit(main()) 
