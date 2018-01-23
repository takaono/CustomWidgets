# -*- coding: utf-8 -*-
import imp
try:
    imp.find_module('PySide2')
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *



class AnyPosCompleter(QCompleter):


    def __init__(self, completions = [], parent=None):
        super(AnyPosCompleter, self).__init__(parent)
        self.local_completion_prefix = ""
        self.source_model = None

        if isinstance(completions, QAbstractItemModel):
            self.setModel(completions)

        elif isinstance(completions, (list, tuple)):
            if len(completions)>0:
                model = QStringListModel(completions)
                self.setModel(model)


    def setModel(self, model):
        self.source_model = model
        super(AnyPosCompleter, self).setModel(self.source_model)


    def updateModel(self):
        local_completion_prefix = self.local_completion_prefix

        class InnerProxyModel(QSortFilterProxyModel):

            def filterAcceptsRow(self, sourceRow, sourceParent):
                index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
                return local_completion_prefix.lower() in self.sourceModel().data(index0, Qt.DisplayRole).lower()

        proxy_model = InnerProxyModel()
        proxy_model.setSourceModel(self.source_model)
        super(AnyPosCompleter, self).setModel(proxy_model)


    def splitPath(self, path):
        self.local_completion_prefix = path
        self.updateModel()
        return ""