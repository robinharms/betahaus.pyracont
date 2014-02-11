from zope.interface import implementer

from betahaus.pyracont.interfaces import IObjectUpdatedEvent
from betahaus.pyracont.interfaces import ISchemaCreatedEvent
from betahaus.pyracont.interfaces import ISchemaBoundEvent


@implementer(IObjectUpdatedEvent)
class ObjectUpdatedEvent(object):
    """ See interfaces.ObjectUpdatedEvent """
    
    def __init__(self, object, fields=(), ):
        self.object = object
        self.fields = fields


@implementer(ISchemaCreatedEvent)
class SchemaCreatedEvent(object):

    def __init__(self, object):
        self.object = object
        

@implementer(ISchemaBoundEvent)
class SchemaBoundEvent(object):

    def __init__(self, object, **kw):
        self.object = object
        self.kw = kw
