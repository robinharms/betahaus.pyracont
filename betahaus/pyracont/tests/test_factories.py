from unittest import TestCase

import colander
from pyramid import testing
from zope.component import createObject
from zope.component.factory import Factory

from betahaus.pyracont.interfaces import ISchemaFactory
from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.interfaces import IFieldFactory
from betahaus.pyracont.interfaces import ISchemaCreatedEvent
from betahaus.pyracont.interfaces import ISchemaBoundEvent
from betahaus.pyracont.tests.fixtures.schemas import DummySchema
from betahaus.pyracont.tests.fixtures.schemas import IDummySchema


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
        
    def tearDown(self):
        testing.tearDown()

    def _register_factory(self, **kw):
        from betahaus.pyracont.factories import SchemaFactory
        params = dict(title = u"dummy schema title",
                      description = u"dummy schema description")
        params.update(kw)
        factory = SchemaFactory(DummySchema, **params)
        self.config.registry.registerUtility(factory, ISchemaFactory, 'DummySchema')

    @property
    def _fut(self):
        from betahaus.pyracont.factories import createSchema
        return createSchema

    def _get_factory(self):
        return self.config.registry.getUtility(ISchemaFactory, 'DummySchema')

    def test_create_object(self):
        """ Should return the same as createSchema. """
        self._register_factory()
        obj = createObject('DummySchema')
        #Note: Instantiated schemas are SchemaNodes themselves!
        self.failUnless(isinstance(obj, colander.SchemaNode))

    def test_create_schema(self):
        self._register_factory()
        obj = self._fut('DummySchema')
        #Note: Instantiated schemas are SchemaNodes themselves!
        self.failUnless(isinstance(obj, colander.SchemaNode))

    def test_title_from_factory(self):
        self._register_factory()
        factory = self._get_factory()
        obj = self._fut('DummySchema')
        self.assertEqual("dummy schema title", obj.title)
        self.assertEqual(factory.title, obj.title)

    def test_description_from_factory(self):
        self._register_factory()
        factory = self._get_factory()
        obj = self._fut('DummySchema')
        self.assertEqual("dummy schema description", obj.description)
        self.assertEqual(factory.description, obj.description)

    def test_provides_declaration_passed_along_to_instance(self):
        self._register_factory(provides = IDummySchema)
        obj = self._fut('DummySchema')
        self.failUnless(IDummySchema.providedBy(obj))

    def test_created_event_sent(self):
        self._register_factory(provides = IDummySchema)
        L = []
        def subscriber(obj, event):
            L.append(event)
        self.config.add_subscriber(subscriber, (IDummySchema, ISchemaCreatedEvent,))
        obj = self._fut('DummySchema')
        self.failUnless(ISchemaCreatedEvent.providedBy(L[0]))

    def test_bound_event_sent(self):
        self._register_factory(provides = IDummySchema)
        L = []
        def subscriber(obj, event):
            L.append(event)
        self.config.add_subscriber(subscriber, (IDummySchema, ISchemaBoundEvent,))
        obj = self._fut('DummySchema', bind = {'dummy': 1})
        self.failUnless(ISchemaBoundEvent.providedBy(L[0]))


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
