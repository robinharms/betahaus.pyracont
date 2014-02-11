import venusian
from zope.component.factory import Factory

from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.interfaces import IFieldFactory
from betahaus.pyracont.interfaces import ISchemaFactory
from betahaus.pyracont.factories import SchemaFactory




class content_factory(object):
    """ Decorator for factories for regular content types """
    venusian = venusian
    
    def __init__(self, factory_name = None, title = u'', description = u'', interfaces = None, provides = None):
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
        name = self.factory_name and self.factory_name or name
        scanner.config.registry.registerUtility(factory, IContentFactory, name = name)

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
        name = self.factory_name and self.factory_name or name
        scanner.config.registry.registerUtility(factory, ISchemaFactory, name = name)


class field_factory(content_factory):
    """ Decorator for factories that create fields. """
    def register(self, scanner, name, wrapped):
        factory = Factory(wrapped,
                          title=self.title,
                          description=self.description,
                          interfaces=self.interfaces)
        name = self.factory_name and self.factory_name or name
        scanner.config.registry.registerUtility(factory, IFieldFactory, name = name)

