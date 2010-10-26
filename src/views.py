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
#        self.header().hide()


class ModelTreeWidgetItem(QTreeWidgetItem):
    def __init__(self,  parent, model_instance):
        super(ModelTreeWidgetItem, self).__init__(parent)
        self.model_instance = model_instance
        self.setText(0, unicode(self.model_instance))



class MachineTree(QTreeWidget):
    tree_structure = (\
        ("machinetype", models.MachineType),
        ("machinemark", models.MachineMark),
        (None, models.Machine)
    )
    modelSelectionChanged = QtCore.pyqtSignal([Model])
    modelSelectionCleared = QtCore.pyqtSignal()


    def __process_node(self, node=None, level=0, parenttreeitem=None):
        if node is None:
            subnodes = self.tree_structure[level][1].all()
        else:
            subnodes = self.tree_structure[level][1].filter(**{self.tree_structure[level-1][0]:node})

        result = []
        for subnode in subnodes:
            result.append(subnode)
            if parenttreeitem is not None:
                treeitem = ModelTreeWidgetItem(parenttreeitem, model_instance=subnode)
            else:
                treeitem = ModelTreeWidgetItem(self,model_instance=subnode )
            if level<len(self.tree_structure)-1:
                result.append(self.__process_node(subnode, level+1, treeitem))
        return result

    def __init__(self, *args, **kwargs):
        super(MachineTree,self).__init__(*args, **kwargs)
#        from pprint import pprint
#        pprint(self.__process_node())
        self.__process_node()
        self.currentItemChanged.connect(self.currentItemChange)
        self.header().hide()

    @QtCore.pyqtSlot("QTreeWidgetItem*", "QTreeWidgetItem*")
    def currentItemChange(self, current, previous):
        self.modelSelectionChanged.emit(current.model_instance)



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


