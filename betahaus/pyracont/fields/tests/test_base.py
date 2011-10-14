from unittest import TestCase

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass


class BaseFieldTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont.fields.base import BaseField
        return BaseField

    def test_verify_class(self):
        from betahaus.pyracont.interfaces import IBaseField
        self.failUnless(verifyClass(IBaseField, self._cut))

    def test_verify_obj(self):
        from betahaus.pyracont.interfaces import IBaseField
        self.failUnless(verifyObject(IBaseField, self._cut()))

    def test_get_raises_not_implemented(self):
        obj = self._cut()
        self.assertRaises(NotImplementedError, obj.get)

    def test_set_raises_not_implemented(self):
        obj = self._cut()
        self.assertRaises(NotImplementedError, obj.set, 'value')

    def test_key_set(self):
        obj = self._cut(key='Hello')
        self.assertEqual(obj.key, 'Hello')
