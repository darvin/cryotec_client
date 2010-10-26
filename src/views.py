# -*- coding: UTF-8 -*-

from qtdjango.detailviews import *
from qtdjango.undetailviews import *
from models import models
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import QRect
from qtdjango.multimodelviews import MultiModelTreeView, ModelTreeWidgetItem

class MachineTreeItem(ModelTreeWidgetItem):
    def __init__(self,  parent, model_instance):
        super(MachineTreeItem, self).__init__(parent, model_instance)
        if model_instance.__class__==models.Machine:
            self.setText(1, unicode(model_instance.client))

class MachineTree(MultiModelTreeView):
    tree_structure = (\
        ("machinetype", models.MachineType),
        ("machinemark", models.MachineMark),
        (None, models.Machine)
    )
    modelSelectionChanged = QtCore.pyqtSignal([Model])
    modelSelectionCleared = QtCore.pyqtSignal()
    item_class = MachineTreeItem

    def __init__(self, *args, **kwargs):
        super(MachineTree,self).__init__(*args, **kwargs)
        self.setColumnCount(2)
        self.expandAll()
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)

class MachinePanel(QFrame):
    def __init__(self):
        super(MachinePanel, self).__init__()
        layout = QVBoxLayout()
        buttonShowAll = QPushButton(u"Показать все")
        self.view = MachineTree()
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
    def filterModelSelected(self, model):
        if model.__class__==models.Machine:
            field_name = "machine"
        elif model.__class__==models.MachineMark:
            field_name = "machine__machinemark"
        elif model.__class__==models.MachineType:
            field_name = "machine__machinemark__machinetype"

        self.set_filter({field_name:model})

    @QtCore.pyqtSlot()
    def filterCleared(self):
        self.set_filter(None)

class FixDetailView(DetailView):
    model = models.Fix

class FixView(TableView):
    model = models.Fix
    sort_by = "-date"
    detail_view = FixDetailView
    fields = ["date", "comment", "report", "fixed", "machine", "user",]

class FixWithButtonsView(ActionView):

    viewclass = FixView


class ReportDetailView(DetailView):
    model = models.Report
    inline_views = ((FixWithButtonsView, "report", u"Ремонты этой неисправности"),)

class ReportView(TableView):
    model = models.Report
    sort_by = "-date"
    fields = ['date', 'comment',  'interest', 'is_fixed', 'maintenance', 'reporttemplate', 'machine', 'user',]
    detail_view = ReportDetailView

class ReportWithButtonsView(ActionView):
    viewclass = ReportView


class MaintenanceDetailView(DetailView):
    model = models.Maintenance
    inline_views = ((ChecklistInlineView, "paction", u"Ответы на чеклист"),)

class MaintenanceView(TableView):
    model = models.Maintenance
    sort_by = "-date"
    fields = ['date', 'comment', 'machine', 'user']
    detail_view = MaintenanceDetailView

class MaintenanceWithButtonsView(ActionView):
    viewclass = MaintenanceView


class CheckupDetailView(DetailView):
    model = models.Checkup

class CheckupView(TableView):
    model = models.Checkup
    sort_by = "-date"
    fields = ['date', 'comment', 'motohours','machine', 'user']
    detail_view = CheckupDetailView

class CheckupWithButtonsView(ActionView):
    viewclass = CheckupView


