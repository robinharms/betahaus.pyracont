from zope.component import getUtility
from zope.component.event import objectEventNotify

from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.interfaces import IFieldFactory
from betahaus.pyracont.interfaces import ISchemaFactory
from betahaus.pyracont.events import SchemaCreatedEvent
from betahaus.pyracont.events import SchemaBoundEvent


def createContent(factory_name, *args, **kwargs):
    """ Works almost the same as createObject.
    """
    return getUtility(IContentFactory, factory_name)(*args, **kwargs)

def createSchema(factory_name, bind = None, **kwargs):
    """ Create a colander schema object. When they're instantiated, they're changed
        to colander.SchemaNode instances.
    """
    factory = getUtility(ISchemaFactory, factory_name)
    schema = factory(**kwargs)
    objectEventNotify(SchemaCreatedEvent(schema))
    if bind:
        schema = schema.bind(**bind)
        objectEventNotify(SchemaBoundEvent(schema, **bind))
    return schema

def createField(factory_name, *args, **kwargs):
    """ Create a field object. """
    return getUtility(IFieldFactory, factory_name)(*args, **kwargs)
