from maya import cmds

from rigs.actions import ActionBuilder, ActionConfig, ActionResponse
from maya_rigs.props import BoolProperty, NodeProperty, NodeListProperty


class ConstrainBuilder(ActionBuilder):
    def build(self, ctx):
        pc = cmds.parentConstraint(ctx['target'], ctx['followers'], mo=ctx['maintainOffset'])
        sc = cmds.scaleConstraint(ctx['target'], ctx['followers'], mo=ctx['maintainOffset'])
        return ActionResponse(200, [])


class ConstrainConfig(ActionConfig):
    @property
    def display_name(self):
        return 'Constrain'

    @property
    def category(self):
        return 'constraints'

    @property
    def properties(self):
        return [
            BoolProperty('maintainOffset'),
            NodeProperty('target'),
            NodeListProperty('followers')
        ]