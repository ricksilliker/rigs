import time
import logging

from rigs.events import EventManager

LOG = logging.getLogger(__name__)


class Sequencer(object):
    Stopped = 0
    Started = 1
    Running = 2
    Finished = 3

    def __init__(self):
        self._steps = []
        self._current_status = None
        self._current_step = None
        self._errors = list()
        self._build_time = 0
        self._process_state = Sequencer.Stopped

    def collect_actions(self):
        all_steps = []
        for step in self._steps:
            all_steps.append(step)
        return all_steps

    def builder(self):
        context = dict()
        yield BuildStatus(group='build', state=BuildStatus.Start)
        yield BuildStatus(group='preprocess', state=BuildStatus.Start)
        EventManager.invoke('preprocessScene', context)
        yield BuildStatus(group='preprocess', state=BuildStatus.Finish)
        yield BuildStatus(group='hierarchy', state=BuildStatus.Start)
        EventManager.invoke('buildHierarchy', context)
        yield BuildStatus(group='hierarchy', state=BuildStatus.Finish)
        yield BuildStatus(group='fetch', state=BuildStatus.Start)
        steps = self.collect_actions()
        yield BuildStatus(group='fetch', state=BuildStatus.Finish)
        yield BuildStatus(group='actions', state=BuildStatus.Start)
        for step in steps:
            yield BuildStatus(group=step.action.display_name, state=BuildStatus.Start)
            self._current_step = step
            step.action.build(context)
            yield BuildStatus(group=step.action.display_name, state=BuildStatus.Finish)
        yield BuildStatus(group='actions', state=BuildStatus.Finish)
        yield BuildStatus(group='cleanup', state=BuildStatus.Start)
        EventManager.invoke('cleanupRig', context)
        yield BuildStatus(group='cleanup', state=BuildStatus.Finish)
        yield BuildStatus(group='optimize', state=BuildStatus.Start)
        EventManager.invoke('optimizeScene', context)
        yield BuildStatus(group='optimize', state=BuildStatus.Finish)
        yield BuildStatus(group='build', state=BuildStatus.Finish)

    def run(self):
        self._process_state = Sequencer.Started
        build_stats = dict()
        runner = self.builder()

        self._process_state = Sequencer.Running
        while self._process_state == Sequencer.Running:
            self._current_status = runner.next()
            group = self._current_status.group
            state = self._current_status.state

            # Record Each group's time of completion.
            if state == BuildStatus.Start:
                build_stats[group]['start'] = time.time()
            elif state == BuildStatus.Finish:
                build_stats[group]['finish'] = time.time()

            # Stop the Sequencer early if an Action has a stats of stop.
            if group == 'actions' and self._current_step and self._current_step.action.status == Step.Stop:
                break

            # Complete the running build if the build group finishes.
            if group == 'build' and state == BuildStatus.Finish:
                break
        self._process_state = Sequencer.Finished
        self._current_step = None

        build_time = build_stats['build']['finish'] - build_stats['build']['start']
        # MAINLOG.indent = 0
        msg = 'Built Rig, {:0.2f} seconds, {1} error(s)'.format(build_time, len(self._errors))
        lvl = logging.WARNING if len(self._errors) else logging.INFO
        LOG.log(lvl, msg)


class Step(object):
    Disabled = 0
    Enabled = 1
    Skip = 2
    Stop = 3

    def __init__(self):
        self._action = None
        self._steps = []
        self._status = Step.Enabled

    @property
    def steps(self):
        for step in self._steps:
            yield step

    @property
    def action(self):
        return self._action

    @property
    def status(self):
        return self._status


class BuildStatus(object):
    Start = 0
    Finish = 1

    settings = dict(
        group=dict(),
        state=dict()
    )

    def __init__(self, **kwargs):
        self._settings = dict()
        for k, v in self.settings.items():
            if k not in kwargs:
                raise KeyError('Missing setting for BuildStatus: %s', k)
            self._settings[k] = v

    def __getattr__(self, item):
        return self._settings[item]
