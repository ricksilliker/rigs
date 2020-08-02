from rigs.actions import ActionProperty

from maya_rigs.core import Node


class StringProperty(ActionProperty):
    @property
    def type(self):
        return str

    def default_value(self):
        return ''


class BoolProperty(ActionProperty):
    @property
    def type(self):
        return bool

    def default_value(self):
        return False


class NodeProperty(ActionProperty):
    @property
    def type(self):
        return Node


class NodeListProperty(ActionProperty):
    @property
    def type(self):
        return list

    def items(self):
        return [NodeProperty]
