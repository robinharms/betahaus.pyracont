from unittest import TestCase

#import colander
from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from betahaus.pyracont.interfaces import ITransformUtil
from betahaus.pyracont.interfaces import ITransformation
from betahaus.pyracont.factories import createSchema


class TransformUtilTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        
    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont.transformation import TransformUtil
        return TransformUtil

    def _fixture(self):
        self.config.scan('betahaus.pyracont.tests.fixtures.schemas')
        self.config.include('betahaus.pyracont.tests.fixtures.transform')
        self.config.registry.settings['transform.transform_out'] = "fake\ndummy"
        self.config.registry.settings['transform.transform_in'] = "fake\ndummy"

    def test_verify_class(self):
        self.failUnless(verifyClass(ITransformUtil, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(ITransformUtil, self._cut()))

    def test_transform_node(self):
        self._fixture()
        util = self._cut()
        appstruct = {}
        chain = ['dummy']
        util.transform_node(appstruct, 'dummy_schema_node', chain, hello = 'world')
        self.assertEqual(appstruct['hello'], 'world')

    def test_transform_node_w_chain(self):
        self._fixture()
        util = self._cut()
        appstruct = {}
        chain = ['dummy', 'fake']
        util.transform_node(appstruct, 'dummy_schema_node', chain, dummy_schema_node = 'world')
        self.assertEqual(appstruct['dummy_schema_node'], 'fake')

    def test_apply_transformations_simple(self):
        self._fixture()
        util = self._cut()
        appstruct = {}
        schema = createSchema('DummySchema')
        util.apply_transformations(appstruct, schema, 'transform_out')
        self.assertEqual(appstruct['dummy_schema_node'], 'fake')

    def test_apply_transformations_w_children(self):
        self._fixture()
        util = self._cut()
        appstruct = {'people': [{'name': 'fredrik', 'contacts': [{'number':'1'}, {'number':'2'}]}]}
        schema = createSchema('DummyPeopleSchema')
        util.apply_transformations(appstruct, schema, 'transform_out')
        self.assertEqual(appstruct['people'][0]['name'], 'fake')
        self.assertEqual(appstruct['people'][0]['contacts'][0]['number'], 'fake')

    def test_output(self):
        self._fixture()
        util = self._cut()
        appstruct = {'people': [{'name': 'fredrik', 'contacts': [{'number':'1'}, {'number':'2'}]}]}
        schema = createSchema('DummyPeopleSchema')
        util.output(appstruct, schema)
        self.assertEqual(appstruct['people'][0]['name'], 'fake')
        self.assertEqual(appstruct['people'][0]['contacts'][0]['number'], 'fake')

    def test_input(self):
        self._fixture()
        util = self._cut()
        appstruct = {'people': [{'name': 'fredrik', 'contacts': [{'number':'1'}, {'number':'2'}]}]}
        schema = createSchema('DummyPeopleSchema')
        util.input(appstruct, schema)
        self.assertEqual(appstruct['people'][0]['name'], 'fake')
        self.assertEqual(appstruct['people'][0]['contacts'][0]['number'], 'fake')

    def test_util_integration(self):
        self.config.include('betahaus.pyracont.transformation')
        self.failUnless(self.config.registry.getUtility(ITransformUtil))


class TransformationTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()
        
    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont.transformation import Transformation
        return Transformation

    def test_verify_class(self):
        self.failUnless(verifyClass(ITransformation, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(ITransformation, self._cut()))
