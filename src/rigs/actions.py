import abc
import logging


LOG = logging.getLogger(__name__)


class ActionBuilder(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.result = None

    @abc.abstractmethod
    def build(self, ctx):
        raise NotImplementedError

    def postBuild(self):
        LOG.debug('Skipping postBuild for Action: %s', self.name)


class ActionConfig(object):
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def display_name(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def category(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def properties(self):
        raise NotImplementedError

    @property
    def build_id(self):
        return 'com.rigs.{0}'.format(self.display_name.lower())

    @property
    def description(self):
        return 'Help message about this Action.'


class ActionProperty(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, title):
        self._title = title

    @property
    @abc.abstractmethod
    def type(self):
        raise NotImplementedError

    @property
    def title(self):
        return self._title

    @property
    def default_value(self):
        return None

    @property
    def choices(self):
        return None

    @property
    def description(self):
        return 'Help message about this ActionProperty.'

    @property
    def items(self):
        return None


class ActionResponse(object):
    def __init__(self, status_code, errors):
        self._status_code = status_code
        self._errors = errors

    def status_code(self):
        return self._status_code

    def errors(self):
        return self._errors
