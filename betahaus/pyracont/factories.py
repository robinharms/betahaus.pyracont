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
    return getUtility(ISchemaFactory, factory_name)(**kwargs)


def createField(factory_name, *args, **kwargs):
    """ Create a field object. """
    return getUtility(IFieldFactory, factory_name)(*args, **kwargs)
