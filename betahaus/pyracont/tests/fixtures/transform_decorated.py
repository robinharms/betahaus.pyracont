from betahaus.pyracont.decorators import transformator
from betahaus.pyracont import Transformation


@transformator()
class Dummy(Transformation):
    name = 'dummy'
    
    def appstruct(self, appstruct, node_name, **kw):
        pass

    def simple(self, value, **kw):
        pass