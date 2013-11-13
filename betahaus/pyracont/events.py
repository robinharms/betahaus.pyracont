from zope.interface import implementer

from betahaus.pyracont.interfaces import IObjectUpdatedEvent

@implementer(IObjectUpdatedEvent)
class ObjectUpdatedEvent(object):
    """ See interfaces.ObjectUpdatedEvent """
    
    def __init__(self, object, fields=(), ):
        self.object = object
        self.fields = fields
