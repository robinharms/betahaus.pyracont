import venusian
from zope.component.factory import Factory
from zope.component import getUtility

from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.interfaces import ISchemaFactory


class content_factory(object):
    """ Decorator for factories for regular content types """
    venusian = venusian
    
    def __init__(self, factory_name, description=u'', interfaces=None):
        self.factory_name = factory_name
        self.description = description
        self.interfaces = interfaces

    def register(self, scanner, name, wrapped):
        factory = Factory(wrapped,
                          title=self.factory_name,
                          description=self.description,
                          interfaces=self.interfaces)
        scanner.config.registry.registerUtility(factory, IContentFactory, self.factory_name)

    def __call__(self, wrapped):
        self.venusian.attach(wrapped, self.register, category='pyracont')
        return wrapped


class schema_factory(content_factory):
    """ Decorator for factories that create colander schemas. """
    def register(self, scanner, name, wrapped):
        factory = Factory(wrapped,
                          title=self.factory_name,
                          description=self.description,
                          interfaces=self.interfaces)
        scanner.config.registry.registerUtility(factory, ISchemaFactory, self.factory_name)
