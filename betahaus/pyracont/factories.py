from zope.component import getUtility

from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.interfaces import IFieldFactory
from betahaus.pyracont.interfaces import ISchemaFactory


def createContent(factory_name, *args, **kwargs):
    """ Works almost the same as createObject.
    """
    return getUtility(IContentFactory, factory_name)(*args, **kwargs)


def createSchema(factory_name, **kwargs):
    """ Create a colander schema object.
    """
    factory = getUtility(ISchemaFactory, factory_name)
    schema = factory(**kwargs)
    schema.title = factory.title
    schema.description = factory.description
    return schema


def createField(factory_name, *args, **kwargs):
    """ Create a field object. """
    return getUtility(IFieldFactory, factory_name)(*args, **kwargs)
