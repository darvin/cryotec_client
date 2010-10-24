# -*- coding: UTF-8 -*-

from qtdjango.detailviews import *
from qtdjango.undetailviews import *
from models import models
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import QRect


class MachineTreeView(TreeView):
    model = models.Machine
    tree = (
            ("customer", models.Client),
            ("machinemark", models.MachineMark),
           )
    fields = "__unicode__"

    def __init__(self, *args, **kwargs):
        super(MachineTreeView, self).__init__(*args, **kwargs)
        self.header().hide()



class MachinePanel(QFrame):
    def __init__(self):
        super(MachinePanel, self).__init__()
        layout = QVBoxLayout()
        buttonShowAll = QPushButton(u"Показать все")
        self.view = MachineTreeView()
        self.setLayout(layout)
        layout.addWidget(buttonShowAll)
        layout.addWidget(self.view)

        buttonShowAll.clicked.connect(self.show_all)

    def show_all(self, checked):
        #FIXME
        self.view.clearSelection()
        self.view.modelSelectionCleared.emit()




class ChecklistInlineView(QFrame, UndetailView):
    model = models.ChecklistAnswer

    def __init__(self, filter):
        """docstring for __init__"""
        QFrame.__init__(self)
        self._widgets =[]
        self.formlayout = QFormLayout()
        self.setLayout(self.formlayout)
        UndetailView.__init__(self, filter)
        self.set_filter(filter)

    def __clean(self):
        """Deletes all old widgets"""
        pass

    def set_filter(self, filter):
        """Creates all widgets when we sets filter"""
        self.__clean()
#        print filter["paction"], "#######"
        machine = filter["paction"].machine
#        print machine
        mmark = machine.machinemark
        questions =[q for q in ChecklistQuestion.filter(machinemark=mmark)]
#        for q in questions:
#            print unicode(q), ChecklistAnswers.filter(maitenance=filter["paction"],\
#                                               checklistquestion=q)


    def save(self):
        pass




class ActionView(UndetailWithButtonsView):
    edit_dumped = False
    edit_filtered_only = True

    def __init__(self, filter):
        """docstring for __init__"""
        super(ActionView, self).__init__(filter)

    @QtCore.pyqtSlot(Model)
    def filterByMachine(self, machine):
        self.set_filter({"machine":machine})

    @QtCore.pyqtSlot()
    def filterCleared(self):
        self.set_filter(None)

class FixDetailView(DetailView):
    model = models.Fix

class FixView(TableView):
    model = models.Fix
    sort_by = "-date"
    detail_view = FixDetailView

class FixWithButtonsView(ActionView):

    viewclass = FixView


class ReportDetailView(DetailView):
    model = models.Report
    inline_views = ((FixWithButtonsView, "report", u"Ремонты этой неисправности"),)

class ReportView(TableView):
    model = models.Report
    sort_by = "-date"
    detail_view = ReportDetailView

class ReportWithButtonsView(ActionView):
    viewclass = ReportView


class MaintenanceDetailView(DetailView):
    model = models.Maintenance
    inline_views = ((ChecklistInlineView, "paction", u"Ответы на чеклист"),)

class MaintenanceView(TableView):
    model = models.Maintenance
    sort_by = "-date"
    detail_view = MaintenanceDetailView

class MaintenanceWithButtonsView(ActionView):
    viewclass = MaintenanceView


class CheckupDetailView(DetailView):
    model = models.Checkup

class CheckupView(TableView):
    model = models.Checkup
    sort_by = "-date"
    detail_view = CheckupDetailView

class CheckupWithButtonsView(ActionView):
    viewclass = CheckupView

