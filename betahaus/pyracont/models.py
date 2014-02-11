from zope.component.factory import Factory
from zope.interface import alsoProvides


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
