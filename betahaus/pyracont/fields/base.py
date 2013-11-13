from persistent import Persistent
from zope.interface import implementer

from betahaus.pyracont.interfaces import IBaseField


@implementer(IBaseField)
class BaseField(Persistent):
    
    def __init__(self, key=None, **kwargs):
        self.key = key

    def get(self, default=None):
        raise NotImplementedError('Must be implemented by subclass')
    
    def set(self, value):
        raise NotImplementedError('Must be implemented by subclass')
