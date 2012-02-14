from unittest import TestCase

import colander
from pyramid import testing
from zope.interface.verify import verifyObject
from zope.component import createObject
from zope.component.factory import Factory

from betahaus.pyracont.interfaces import ISchemaFactory
from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.interfaces import IFieldFactory
from betahaus.pyracont.tests.fixtures.schemas import DummySchema


class CreateContentTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self._register_factory()
        
    def tearDown(self):
        testing.tearDown()

    def _register_factory(self):
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
        factory = Factory(DummySchema, 'DummySchema')
        factory.title = u"dummy schema title"
        factory.description = u"dummy schema description"
        self.config.registry.registerUtility(factory, ISchemaFactory, 'DummySchema')

    @property
    def _fut(self):
        from betahaus.pyracont.factories import createSchema
        return createSchema

    def _get_factory(self):
        return self.config.registry.getUtility(ISchemaFactory, 'DummySchema')

    def test_create_object(self):
        """ Should return the same as createSchema. """
        obj = createObject('DummySchema')
        #Note: Instantiated schemas are SchemaNodes themselves!
        self.failUnless(isinstance(obj, colander.SchemaNode))

    def test_create_schema(self):
        obj = self._fut('DummySchema')
        #Note: Instantiated schemas are SchemaNodes themselves!
        self.failUnless(isinstance(obj, colander.SchemaNode))

    def test_title_from_factory(self):
        factory = self._get_factory()
        obj = self._fut('DummySchema')
        self.assertEqual("dummy schema title", obj.title)
        self.assertEqual(factory.title, obj.title)

    def test_description_from_factory(self):
        factory = self._get_factory()
        obj = self._fut('DummySchema')
        self.assertEqual("dummy schema description", obj.description)
        self.assertEqual(factory.description, obj.description)


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
