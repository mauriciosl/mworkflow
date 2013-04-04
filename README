
=== MWorkflow ===

Part of the M project
MWorkflow is a simple (to use) workflow for python

== defining a workflow ==

<code>
from mworkflow import Workflow, State, StartState, EndState

class PublishWorkflow(Workflow):

    start = StartState()
    rascunho = State('Rascunho', 'criar', 'salvar')
    publicado = State('Publicado', 'publicar', 're-publicar')
    despublicado = State('Despublicado', 'despublicar')
    end = EndState('excluir')

    start >> rascunho >> publicado >> despublicado >> end
    rascunho >> rascunho
    publicado >> publicado
</code>

== Using a workflow ==

<code>

p = PublishWorkflow()

</code>

