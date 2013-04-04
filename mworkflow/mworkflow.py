#
# encoding: utf-8


class State(object):
    """Creates a State
    arguments:
        name
            The state's name
        transition_name=None
            The transition to this state name
        re_transition_name=None
            The transition from this state to itself name
    """

    def __init__(self, name, transition_name=None, re_transition_name=None):
        self.name = name
        self.transition_name = transition_name
        self.re_transition_name = re_transition_name
        self._allowed_transitions = {}

    def verb(self):
        """Returns the verb"""
        return self.transition_name

    def reverb(self):
        """Returns the verb to itself"""
        return self.re_transition_name

    def add_transition(self, transition):
        """Adds a transition to this state"""
        self._allowed_transitions[transition.destination] = transition

    def get_transitions(self):
        """Returns all available transitions from this state"""
        return self._allowed_transitions.values()

    def get_possible_states(self):
        """Returns all possible state changes from this state"""
        return self._allowed_transitions.keys()

    def __rshift__(self, other):
        """>> operator, describes a transition from this state to other state"""
        verb = self.verb()
        if self == other:
            verb = self.reverb()
        transition = Transition(self, other, verb)
        self.add_transition(transition)
        return other

    def __unicode__(self):
        return unicode(self.name)

    __str__ = __repr__ = __unicode__


class BaseWorkflow(type):

    def __new__(cls, name, bases, attrs):
        states = []
        for key, value in attrs.items():
            if isinstance(value, State):
                states.append(value)
        attrs['_states'] = states
        return type.__new__(cls, name, bases, attrs)


class Workflow(object):
    __metaclass__ = BaseWorkflow

    def __init__(self):
        self.current_state = self.start

    def get_transitions(self):
        """Returns possible transitions from this state"""
        return self.current_state.get_transitions()

    def get_possible_states(self):
        """Returns possible states from this state"""
        return self.current_state.get_possible_states()

    def transit(self, destination):
        """Change the state of this workflow instance if allowed"""
        if destination not in self.get_possible_states():
            raise ValueError(u"Invalid destination %s" % destination)
        self.current_state = destination

    @property
    def states(self):
        """States of this workflow"""
        return self._states

    def get_state(self):
        return self.current_state

    def set_state(self, new_state):
        self.current_state = new_state
        return new_state

    state = property(get_state, set_state)


class Transition(object):
    """An object that describes a transition from a state to another"""
    def __init__(self, origin, destination, verb):
        self.origin = origin
        self.destination = destination
        self.verb = verb

    def __unicode__(self):
        return u"%s >[%s]> %s" % (self.origin, self.verb, self.destination)
    __str__ = __repr__ = __unicode__


class StartState(State):
    """A special state to describe the starting point of an workflow"""

    def __init__(self):
        super(StartState, self).__init__('Start', 'Start', 'ReStart')


class EndState(State):
    """A special state to describe the end point of an workflow"""

    def __init__(self, transition_name=None):
        transition_name = transition_name or 'delete'
        super(EndState, self).__init__('End', transition_name)
