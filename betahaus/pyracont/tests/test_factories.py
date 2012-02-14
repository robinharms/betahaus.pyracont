from unittest import TestCase

import colander
from pyramid import testing
from zope.interface.verify import verifyObject
from zope.component import createObject
from zope.component.factory import Factory

from betahaus.pyracont.tests.fixtures.schemas import DummySchema


class CreateContentTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self._register_factory()
        
    def tearDown(self):
        testing.tearDown()

    def _register_factory(self):
        from betahaus.pyracont.interfaces import IContentFactory
        factory = Factory(testing.DummyModel, 'DummyModel')
        self.config.registry.registerUtility(factory, IContentFactory, 'DummyModel')

    @property
    def _fut(self):
        from betahaus.pyracont.factories import createContent
        return createContent

    def test_create_object(self):
        """ Should return the same as createContent. """
        obj = createObject('DummyModel')
        self.failUnless(isinstance(obj, testing.DummyModel))

    def test_create_content(self):
        obj = self._fut('DummyModel')
        self.failUnless(isinstance(obj, testing.DummyModel))


class CreateSchemaTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self._register_factory()
        
    def tearDown(self):
        testing.tearDown()

    def _register_factory(self):
        from betahaus.pyracont.interfaces import ISchemaFactory
        factory = Factory(DummySchema, 'DummySchema')
        self.config.registry.registerUtility(factory, ISchemaFactory, 'DummySchema')

    @property
    def _fut(self):
        from betahaus.pyracont.factories import createSchema
        return createSchema

    def test_create_object(self):
        """ Should return the same as createSchema. """
        obj = createObject('DummySchema')
        #Note: Instantiated schemas are SchemaNodes themselves!
        self.failUnless(isinstance(obj, colander.SchemaNode))

    def test_create_schema(self):
        obj = self._fut('DummySchema')
        #Note: Instantiated schemas are SchemaNodes themselves!
        self.failUnless(isinstance(obj, colander.SchemaNode))
        # check title and description
        self.assertIsNotNone(obj.title)
        self.assertIsNotNone(obj.decription)


class CreateFieldTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self._register_factory()
        
    def tearDown(self):
        testing.tearDown()

    @property
    def _field_cls(self):
        from betahaus.pyracont.fields.base import BaseField
        return BaseField

    def _register_factory(self):
        from betahaus.pyracont.interfaces import IFieldFactory
        factory = Factory(self._field_cls, 'BaseField')
        self.config.registry.registerUtility(factory, IFieldFactory, 'BaseField')

    @property
    def _fut(self):
        from betahaus.pyracont.factories import createField
        return createField

    def test_create_object(self):
        """ Should return the same as createField. """
        obj = createObject('BaseField')
        self.failUnless(isinstance(obj, self._field_cls))

    def test_create_field(self):
        obj = self._fut('BaseField')
        self.failUnless(isinstance(obj, self._field_cls))
