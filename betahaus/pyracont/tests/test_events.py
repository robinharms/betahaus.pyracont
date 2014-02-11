from unittest import TestCase

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass

from betahaus.pyracont.interfaces import IObjectUpdatedEvent
from betahaus.pyracont.interfaces import ISchemaCreatedEvent
from betahaus.pyracont.interfaces import ISchemaBoundEvent


class ObjectUpdatedEventTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont.events import ObjectUpdatedEvent
        return ObjectUpdatedEvent

    def test_verify_class(self):
        self.failUnless(verifyClass(IObjectUpdatedEvent, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(IObjectUpdatedEvent, self._cut(object())))


class SchemaCreatedEventTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont.events import SchemaCreatedEvent
        return SchemaCreatedEvent

    def test_verify_class(self):
        self.failUnless(verifyClass(ISchemaCreatedEvent, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(ISchemaCreatedEvent, self._cut(object())))


class SchemaBoundEventTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont.events import SchemaBoundEvent
        return SchemaBoundEvent

    def test_verify_class(self):
        self.failUnless(verifyClass(ISchemaBoundEvent, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(ISchemaBoundEvent, self._cut(object())))
