from zope.component import getUtility
from zope.component.event import objectEventNotify
from zope.component.factory import Factory
from zope.interface import alsoProvides

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


class SchemaFactory(Factory):

    def __init__(self, callable, title = '', description = '', interfaces = None, provides = None):
        super(SchemaFactory, self).__init__(callable, title=title, description=description, interfaces=interfaces)
        self.provides = provides

    def __call__(self, *args, **kw):
        obj = self._callable(*args, **kw)
        if self.provides:
            alsoProvides(obj, self.provides)
        obj.title = kw.pop('title', self.title)
        obj.description = kw.pop('description', self.description)
        return obj
