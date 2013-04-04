
MWorkflow
=========

Part of the M project
MWorkflow is a simple (to use) workflow for python

Defining a Workflow
-------------------

    from mworkflow import Workflow, State, StartState, EndState

    class PublishWorkflow(Workflow):

        start = StartState()
        draft = State('Draft', 'create')
        published = State('Published', 'publish', 're-publish')
        unpublished = State('Unpublished', 'unpublish')
        end = EndState('delete')

        start >> draft >> published >> unpublished >> end
        published >> published
        unpublished >> published

Using a workflow
----------------

    p = PublishWorkflow()
    p.do_create() // do_<trasition verb> will activate the transition to another state
    p.transit('Published') // you can pass the name of the state you want to change
    p.transit('U') // you can use de first letter of the state
    p.do_create() // raises an Exception as its not permited to go from Unpublished to draft
    p = PublishWorkflow(PublishWorkflow.published) // start at some state
    p.allowed_transitions() // allowed actions [<Transition unpublish>, <Transition re-publish>]
    p.allowed_states() // allowed transition states objects [<State Published>, <State Unpublished>]

Listening to events
-------------------

    PublishWorkflow.add_change_listener(myCallback) // callback to any changes
    PublishWorkflow.add_publish_listener(myCallback) // callback to when workflow is published
    PublishWorkflow.add_listener('Unpublished', myCallback) // callback to when the workflow reach the unpublished state
