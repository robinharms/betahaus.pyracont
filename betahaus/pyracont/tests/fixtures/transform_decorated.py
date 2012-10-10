from betahaus.pyracont.decorators import transformator
from betahaus.pyracont import Transformation


@transformator()
class Dummy(Transformation):
    name = 'dummy'
    
    def __call__(self, appstruct, node_name, **kw):
        pass
