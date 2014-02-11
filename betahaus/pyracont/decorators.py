import venusian
from zope.component.factory import Factory
from zope.component import getUtility
from zope.interface.verify import verifyClass

from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.interfaces import IFieldFactory
from betahaus.pyracont.interfaces import ISchemaFactory
from betahaus.pyracont.models import SchemaFactory




class content_factory(object):
    """ Decorator for factories for regular content types """
    venusian = venusian
    
    def __init__(self, factory_name, title=u'', description=u'', interfaces=None, provides = None):
        self.factory_name = factory_name
        self.title = title
        self.description = description
        self.interfaces = interfaces
        self.provides = provides

    def register(self, scanner, name, wrapped):
        title = self.title and self.title or self.factory_name
        factory = Factory(wrapped,
                          title=title,
                          description=self.description,
                          interfaces=self.interfaces)
        scanner.config.registry.registerUtility(factory, IContentFactory, self.factory_name)

    def __call__(self, wrapped):
        self.venusian.attach(wrapped, self.register, category='pyracont')
        return wrapped


class schema_factory(content_factory):
    """ Decorator for factories that create colander schemas. """
    def register(self, scanner, name, wrapped):
        factory = SchemaFactory(wrapped,
                          title=self.title,
                          description=self.description,
                          interfaces=self.interfaces,
                          provides=self.provides)
        scanner.config.registry.registerUtility(factory, ISchemaFactory, self.factory_name)


class field_factory(content_factory):
    """ Decorator for factories that create fields. """
    def register(self, scanner, name, wrapped):
        factory = Factory(wrapped,
                          title=self.title,
                          description=self.description,
                          interfaces=self.interfaces)
        scanner.config.registry.registerUtility(factory, IFieldFactory, self.factory_name)

