from zope.interface import implements

from betahaus.pyracont.interfaces import IObjectUpdatedEvent


class ObjectUpdatedEvent(object):
    __doc__ = IObjectUpdatedEvent.__doc__
    implements(IObjectUpdatedEvent)
    
    def __init__(self, object, fields=(), ):
        self.object = object
        self.fields = fields
