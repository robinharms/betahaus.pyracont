from betahaus.pyracont.transformation import Transformation
from betahaus.pyracont.interfaces import ITransformation


class _DummyTransformation(Transformation):
    def appstruct(self, appstruct, node_name, **kw):
        appstruct.update(**kw)

    def simple(self, value, **kw):
        return "*%s*" % value


class _FakeTransformation(Transformation):
    def appstruct(self, appstruct, node_name, **kw):
        appstruct[node_name] = 'fake'

    def simple(self, value, **kw):
        return 'fake'


def includeme(config):
    config.registry.registerUtility(_DummyTransformation(), name = 'dummy')
    config.registry.registerUtility(_FakeTransformation(), name = 'fake')
