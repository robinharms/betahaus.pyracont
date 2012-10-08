from betahaus.pyracont.transformation import Transformation
from betahaus.pyracont.interfaces import ITransformation


class _DummyTransformation(Transformation):
    def __call__(self, appstruct, node_name, **kw):
        appstruct.update(**kw)


class _FakeTransformation(Transformation):
    def __call__(self, appstruct, node_name, **kw):
        appstruct[node_name] = 'fake'


def includeme(config):
    config.registry.registerUtility(_DummyTransformation(), name = 'dummy')
    config.registry.registerUtility(_FakeTransformation(), name = 'fake')
