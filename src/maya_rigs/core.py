from maya.api import OpenMaya


class Node(object):
    def __init__(self, mobject):
        self._node = mobject

    def __str__(self):
        return OpenMaya.MFnDagNode(self._node).fullPathName()
