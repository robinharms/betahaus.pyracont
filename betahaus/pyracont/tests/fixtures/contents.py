from betahaus.pyracont.decorators import content_factory


@content_factory('DummyContent')
class DummyContent(object):
    
    def __init__(self, *args, **kwargs):
        setattr(self, 'args', args)
        setattr(self, 'kwargs', kwargs)
