from hashlib import sha1

from zope.interface import implements
from betahaus.pyracont.fields.base import BaseField
from betahaus.pyracont.interfaces import IPasswordField
from betahaus.pyracont.decorators import field_factory
from repoze.folder import unicodify


def get_sha_password(password):
    """ Encode a plaintext password to sha1. """
    if isinstance(password, unicode):
        password = password.encode('UTF-8')
    return 'SHA1:' + sha1(password).hexdigest()


_marker = object()


@field_factory('PasswordField')
class PasswordField(BaseField):
    """ Field that stores hash of passed value. """
    implements(IPasswordField)

    def __init__(self, key=None, hash_method=None, **kwargs):
        super(PasswordField, self).__init__(key=key, **kwargs)
        self.__encrypted_password__ = None
        min_length = kwargs.get('min_length', 5)
        assert isinstance(min_length, int)
        self.min_length = min_length
        
        if hash_method is None:
            hash_method = get_sha_password
        assert callable(hash_method)
        self.hash_method = hash_method

    def get(self, default=None):
        pw = self.__encrypted_password__
        if pw is None:
            return default
        return pw

    def set(self, value):
        if not isinstance(value, unicode):
            value = unicodify(value)
        if not len(value) >= self.min_length:
            raise ValueError("Password shorter than required %s chars" % self.min_length)
        self.__encrypted_password__ = self.hash_method(value)

    def check_input(self, value):
        if not isinstance(value, basestring):
            raise TypeError("check_input only accepts strings as input, got %s" % value)
        encrypted = self.get(default=_marker)
        if encrypted is _marker:
            return False
        if not isinstance(value, unicode):
            value = unicodify(value)
        return self.hash_method(value) == encrypted

    def clear_password(self):
        self.__encrypted_password__ = None
