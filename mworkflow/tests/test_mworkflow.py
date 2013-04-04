#
# encoding: utf-8

from unittest import TestCase
from mworkflow import Workflow, State, StartState, EndState


class TestWorkflow(TestCase):

    def setUp(self):
        class FakeWorkflow(Workflow):
            start = StartState()
            fake = State('Fake')
            other = State('Other')
            end = EndState()
            start >> fake >> other >> end
        self.f = FakeWorkflow()

    def test_state_definition(self):
        assert self.f.fake in self.f._states

    def test_set_state(self):
        self.f.set_state(self.f.other)
        assert self.f.current_state == self.f.other


class TestWorkflowTransition(TestCase):

    def setUp(self):
        class FakeWorkflow(Workflow):
            start = StartState()
            fake = State('Fake')
            other = State('Other')
            end = EndState()
            start >> fake >> other >> end
            start >> other
        self.f = FakeWorkflow()

    def test_get_possible_states_at_start(self):
        for state in [self.f.fake, self.f.other]:
            assert state in self.f.get_possible_states(), ("%s should be possible" % state)

    def test_get_possible_states_at_fake(self):
        self.f.state = self.f.fake
        assert self.f.other in self.f.get_possible_states(), "other state should be possible"
        assert self.f.fake not in self.f.get_possible_states(), "fake state should not be one of the possible states"

    def test_get_possible_states_at_other(self):
        self.f.state = self.f.other
        assert self.f.end in self.f.get_possible_states(), "only the end should be possible after 'other' state"

    def test_get_possible_states_at_end(self):
        self.f.state = self.f.end
        assert not self.f.get_possible_states(), "there should be no state possible after the end..."
