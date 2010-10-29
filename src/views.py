# -*- coding: UTF-8 -*-

from qtdjango.detailviews import *
from qtdjango.undetailviews import *
from models import models
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import QRect
from qtdjango.multimodelviews import MultiModelTreeView, ModelTreeWidgetItem, ModelInfoView


class MachineTreeItem(ModelTreeWidgetItem):
    icons = {"Machine":"brick.png",
             "MachineMark":"bricks.png",
             "MachineType":"bricks_lot.png",
    }
    def __init__(self,  parent, model_instance):
        super(MachineTreeItem, self).__init__(parent, model_instance)
        if model_instance.__class__==models.Machine:
            self.setText(1, unicode(model_instance.client))

        i = QIcon(":/small_icons/"+self.icons[model_instance.__class__.__name__])
        self.setIcon(0, i)

class MachineTree(MultiModelTreeView):
    tree_structure = (\
        ("machinetype", models.MachineType),
        ("machinemark", models.MachineMark),
        (None, models.Machine)
    )
    modelSelectionChanged = QtCore.pyqtSignal([Model])
    modelSelectionCleared = QtCore.pyqtSignal()
    item_class = MachineTreeItem
    models = (models.MachineType, models.MachineMark, models.Machine)

    def __init__(self, *args, **kwargs):
        super(MachineTree,self).__init__(*args, **kwargs)
        self.setColumnCount(2)

    def refresh(self):
        super(MachineTree,self).refresh()
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

        machine = filter["maintenance"].machine

        mmark = machine.machinemark
        self.questions =[q for q in models.ChecklistQuestion.all() if mmark in q.machinemark]
        self.answers = []
        for q in self.questions:
            try:
                answer = models.ChecklistAnswer.filter(maintenance=filter["maintenance"],\
                                               checklistquestion=q)[0]
            except IndexError:
                answer = models.ChecklistAnswer.new()
                answer.maintenance=filter["maintenance"]
                answer.checklistquestion=q

            self.answers.append(answer)


            q_str = q.comment
            if q.required:
                q_str = u"<b>%s</b>" % q_str

            w = TextEditWidget(models.ChecklistAnswer.comment)
            w.setData(answer.comment)
            self._widgets.append(w)
            self.formlayout.addRow(QtCore.QString.fromUtf8(q_str), w)


    def save(self):
        for q, a, w in zip(self.questions, self.answers, self._widgets):
            a.comment = w.getData()
            a.save()

    def clean(self):
        """Cleans temporary models of view"""
        for answer in self.answers:
            answer.delete()




class ActionView(UndetailWithButtonsView):
    edit_dumped = False
    edit_filtered_only = True
    icons_for_button = {
        "edit":"pencil.png",
        "delete":"delete.png",
        "new":"add.png",
    }
    def __init__(self, filter):
        """docstring for __init__"""
        super(ActionView, self).__init__(filter)

        for buttonname, iconname in self.icons_for_button.items():
            self._buttons[buttonname].setIcon(QIcon(":/small_icons/"+iconname))

    def get_buttons_state(self, model_selected=None):
        f = self.view.filter
        if f is not None:
            if "machine" in f.keys() or "report" in f.keys() or "maintenance" in f.keys():
                return super(ActionView, self).get_buttons_state(model_selected)
        return {"edit":False, "delete":False, "new":False}


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

    def set_filter(self, filter):


        if filter is not None:
            try:
                self._widgets["report"].set_filter({"machine":filter["machine"]})
            except KeyError:
                pass
        super(FixDetailView, self).set_filter(filter)

class FixView(TableView):
    model = models.Fix
    sort_by = "-date"
    detail_view = FixDetailView
    fields = ["date", "comment", "report", "fixed", "machine", "user",]
    def set_filter(self, filter):
        if filter is not None:
            if "report" in filter.keys():
                filter["machine"]=filter["report"].machine
        super(FixView, self).set_filter(filter)


    def create_model_instance(self):
        m = super(FixView,self).create_model_instance()
        m.machine = self.filter["machine"]
        return m

class FixWithButtonsView(ActionView):

    viewclass = FixView


class ReportDetailView(DetailView):
    model = models.Report
#    inline_views = ((FixWithButtonsView, "report", u"Ремонты этой неисправности"),)

    def set_filter(self, filter):
        super(ReportDetailView, self).set_filter(filter)
        if filter is not None:
            self._widgets["maintenance"].set_filter({"machine":filter["machine"]})


class ReportView(TableView):
    model = models.Report
    sort_by = "-date"
    fields = ['date', 'comment',  'interest', 'is_fixed', 'maintenance', 'reporttemplate', 'machine', 'user',]
    detail_view = ReportDetailView
    def create_model_instance(self):
        m = super(ReportView,self).create_model_instance()
        m.machine = self.filter["machine"]
        return m

    def set_filter(self, filter):
        if filter is not None:
            if "maintenance" in filter.keys():
                filter["machine"]=filter["maintenance"].machine
        super(ReportView, self).set_filter(filter)

class ReportWithButtonsView(ActionView):
    viewclass = ReportView


class MaintenanceDetailView(DetailView):
    model = models.Maintenance
    inline_views = ((ChecklistInlineView, "maintenance", u"Ответы на чеклист"),)

class MaintenanceView(TableView):
    model = models.Maintenance
    sort_by = "-date"
    fields = ['date', 'comment', 'machine', 'user']
    detail_view = MaintenanceDetailView
    def create_model_instance(self):
        m = super(MaintenanceView,self).create_model_instance()
        m.machine = self.filter["machine"]
        return m

class MaintenanceWithButtonsView(ActionView):
    viewclass = MaintenanceView


class CheckupDetailView(DetailView):
    model = models.Checkup

class CheckupView(TableView):
    model = models.Checkup
    sort_by = "-date"
    fields = ['date', 'comment', 'motohours','machine', 'user']
    detail_view = CheckupDetailView
    def create_model_instance(self):
        m = super(CheckupView,self).create_model_instance()
        m.machine = self.filter["machine"]
        return m

class CheckupWithButtonsView(ActionView):
    viewclass = CheckupView


class InfoView(ModelInfoView):
    models = models.models