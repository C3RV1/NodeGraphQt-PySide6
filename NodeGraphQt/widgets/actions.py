#!/usr/bin/python
from qtpy import QtCore, QtWidgets
from .stylesheet import STYLE_QMENU


class BaseMenu(QtWidgets.QMenu):

    def __init__(self, *args, **kwargs):
        super(BaseMenu, self).__init__(*args, **kwargs)
        self.setStyleSheet(STYLE_QMENU)
        self.node_class = None
        self.graph = None

    # disable for issue #142
    # def hideEvent(self, event):
    #     super(BaseMenu, self).hideEvent(event)
    #     for a in self.actions():
    #         if hasattr(a, 'node_id'):
    #             a.node_id = None

    def get_menu(self, name, node_id=None):
        for child in self.children():
            if isinstance(child, BaseMenu):
                if child.title() == name:
                    return child
                if node_id and child.node_class:
                    node = child.graph.get_node_by_id(node_id)
                    if isinstance(node, child.node_class):
                        return child

    def get_menus(self, node_class):
        menus = []
        for child in self.children():
            if isinstance(child, BaseMenu):
                if child.node_class:
                    if issubclass(child.node_class, node_class):
                        menus.append(child)
        return menus


class GraphAction(QtWidgets.QAction):

    executed = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(GraphAction, self).__init__(*args, **kwargs)
        self.graph = None
        self.triggered.connect(self._on_triggered)

    def _on_triggered(self):
        self.executed.emit(self.graph)

    def get_action(self, name):
        for action in self.qmenu.actions():
            if not action.parent() and action.text() == name:
                return action


class NodeAction(GraphAction):

    executed = QtCore.Signal(object, object)

    def __init__(self, *args, **kwargs):
        super(NodeAction, self).__init__(*args, **kwargs)
        self.node_id = None

    def _on_triggered(self):
        node = self.graph.get_node_by_id(self.node_id)
        self.executed.emit(self.graph, node)
