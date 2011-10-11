from unittest import TestCase

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass

def _dummy_hash_method(text):
    """ Dummy method that appends '-1' to every string...
    """
    return "%s-1" % text


class PasswordFieldTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont.fields.password import PasswordField
        return PasswordField

    def test_verify_class(self):
        from betahaus.pyracont.interfaces import IPasswordField
        self.failUnless(verifyClass(IPasswordField, self._cut))

    def test_verify_obj(self):
        from betahaus.pyracont.interfaces import IPasswordField
        self.failUnless(verifyObject(IPasswordField, self._cut()))

    def test_with_default_hash(self):
        """ Set is almost same as add. Important for compatibility when field is not directly accessed. """
        obj = self._cut()
        obj.set('hello')
        self.failUnless(obj.get().startswith('SHA1'))

    def test_custom_hash_method(self):
        obj = self._cut(hash_method = _dummy_hash_method)
        obj.set('hello')
        self.assertEqual(obj.get(), 'hello-1')

    def test_min_length(self):
        obj = self._cut(min_length = 100)
        self.assertRaises(ValueError, obj.set, 'hello')
