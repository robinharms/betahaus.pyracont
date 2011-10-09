from unittest import TestCase

import colander
from pyramid import testing

from betahaus.pyracont.tests.fixtures.contents import DummyContent
from betahaus.pyracont.tests.fixtures.override_content import OtherContent
from betahaus.pyracont.tests.fixtures.schemas import DummySchema
from betahaus.pyracont.tests.fixtures.override_schema import OtherSchema


class DecoratorContentFactoryTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.scan('betahaus.pyracont.tests.fixtures.contents')

    def tearDown(self):
        testing.tearDown()
    
    def _create_content(self, name):
        from betahaus.pyracont.interfaces import IContentFactory
        return self.config.registry.getUtility(IContentFactory, name)()

    def test_content_registered(self):
        obj = self._create_content('DummyContent')
        self.failUnless(isinstance(obj, DummyContent))

    def test_override_registered(self):
        self.config.scan('betahaus.pyracont.tests.fixtures.override_content')
        obj = self._create_content('DummyContent')
        self.failUnless(isinstance(obj, OtherContent))


class DecoratorSchemaFactoryTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.scan('betahaus.pyracont.tests.fixtures.schemas')

    def tearDown(self):
        testing.tearDown()

    def _create_schema(self, name):
        from betahaus.pyracont.interfaces import ISchemaFactory
        return self.config.registry.getUtility(ISchemaFactory, name)()

    def test_content_registered(self):
        #Note: Instances of colander.Schema are colander.SchemaNode objects!
        obj = self._create_schema('DummySchema')
        self.failUnless('dummy_schema_node' in obj)

    def test_override_registered(self):
        #Note: Instances of colander.Schema are colander.SchemaNode objects!
        self.config.scan('betahaus.pyracont.tests.fixtures.override_schema')
        obj = self._create_schema('DummySchema')
        self.failUnless('other_schema_node' in obj)


class DecoratorFieldFactoryTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.scan('betahaus.pyracont.fields.versioning')

    def tearDown(self):
        testing.tearDown()

    def _create_field(self, name):
        from betahaus.pyracont.interfaces import IFieldFactory
        return self.config.registry.getUtility(IFieldFactory, name)()

    def test_content_registered(self):
        obj = self._create_field('VersioningField')
        from betahaus.pyracont.interfaces import IBaseField
        self.failUnless(IBaseField.providedBy(obj))
