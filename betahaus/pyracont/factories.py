from zope.component import getUtility

from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.interfaces import ISchemaFactory


def createContent(factory_name, *args, **kwargs):
    """ Works almost the same as createObject.
    """
    return getUtility(IContentFactory, factory_name)(*args, **kwargs)


def createSchema(factory_name, context, request, **kwargs):
    """ Create a colander schema object.
        context, request and kwargs are for bind, which occurs
        after object construction. Hence this factory works a bit
        different than the standard one.
        See the colander documentation for information on schema bind.
    """
    #Note: bind() returns a bound schema, so it's not done in place .)
    schema = getUtility(ISchemaFactory, factory_name)()
    return schema.bind(context=context,
                request=request,
                **kwargs)