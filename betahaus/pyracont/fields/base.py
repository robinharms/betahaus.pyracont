from persistent import Persistent
from zope.interface import implements

from betahaus.pyracont.interfaces import IBaseField


class BaseField(Persistent):
    implements(IBaseField)
    
    def __init__(self, key=None, **kwargs):
        self.key = key

    def get(self, default=None):
        raise NotImplementedError('Must be implemented by subclass')
    
    def set(self, value):
        raise NotImplementedError('Must be implemented by subclass')
