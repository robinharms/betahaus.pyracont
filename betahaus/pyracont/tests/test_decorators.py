from unittest import TestCase

from pyramid import testing

from betahaus.pyracont.interfaces import ISchemaFactory
from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.tests.fixtures.contents import DummyContent
from betahaus.pyracont.tests.fixtures.override_content import OtherContent
from betahaus.pyracont.tests.fixtures.schemas import IDummySchema


class DecoratorContentFactoryTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.scan('betahaus.pyracont.tests.fixtures.contents')

    def tearDown(self):
        testing.tearDown()
    
    def _create_content(self, name):
        return self.config.registry.getUtility(IContentFactory, name)()

    def test_content_registered(self):
        obj = self._create_content('DummyContent')
        self.failUnless(isinstance(obj, DummyContent))

    def test_override_registered(self):
        self.config.scan('betahaus.pyracont.tests.fixtures.override_content')
        obj = self._create_content('DummyContent')
        self.failUnless(isinstance(obj, OtherContent))

    def test_name_taken_from_class_if_not_specified(self):
        self.failUnless(self.config.registry.queryUtility(IContentFactory, name = 'SomeInterestingContent'))


class DecoratorSchemaFactoryTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.scan('betahaus.pyracont.tests.fixtures.schemas')

    def tearDown(self):
        testing.tearDown()

    def _create_schema(self, name):
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

    def _get_factory(self):
        return self.config.registry.getUtility(ISchemaFactory, 'DummySchema')

    def test_title_picked_up(self):
        obj = self._get_factory()
        self.assertEqual(obj.title, u"dummy schema title")

    def test_description_picked_up(self):
        obj = self._get_factory()
        self.assertEqual(obj.description, u"dummy schema description")

    def test_provides_declaration_passed_along_to_instance(self):
        obj = self._create_schema('DummySchema')
        self.failUnless(IDummySchema.providedBy(obj))


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

