from unittest import TestCase
from datetime import datetime

import colander
from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass
from zope.component.factory import Factory
from zope.component.interfaces import ComponentLookupError
from BTrees.OOBTree import OOBTree

from betahaus.pyracont.exceptions import CustomFunctionLoopError


class MockSchema(colander.Schema):
    title = colander.SchemaNode(colander.String())
    userid = colander.SchemaNode(colander.String())
    created = colander.SchemaNode(colander.DateTime())


class BaseFolderTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont import BaseFolder
        return BaseFolder

    def _now(self):
        from betahaus.pyracont import utcnow
        return utcnow()

    def _custom_versionging_field_fixture(self):
        self.config.scan('betahaus.pyracont.fields.versioning')
        
        class DummyCls(self._cut):
            custom_fields = {'test':'VersioningField'}
        
        return DummyCls

    def test_verify_class(self):
        from betahaus.pyracont.interfaces import IBaseFolder
        self.failUnless(verifyClass(IBaseFolder, self._cut))

    def test_verify_obj(self):
        from betahaus.pyracont.interfaces import IBaseFolder
        self.failUnless(verifyObject(IBaseFolder, self._cut()))

    def test_title_property(self):
        obj = self._cut(title='Hello world')
        self.assertEqual(obj.title, 'Hello world')

    def test_created_property(self):
        now = self._now()
        obj = self._cut(created=now)
        self.assertEqual(obj.created, now)

    def test_modified_property(self):
        now = self._now()
        obj = self._cut(modified=now)
        self.assertEqual(obj.modified, now)
    
    def test_uid_property(self):
        obj = self._cut()
        self.assertEqual(len(obj.uid), 36)
        obj = self._cut(uid='set_uid_this_way')
        self.assertEqual(obj.uid, 'set_uid_this_way')

    def test_suggest_name_empty_context(self):
        parent = self._cut()
        obj = self._cut(title="Store me")
        self.assertEqual(obj.suggest_name(parent), 'store-me')
    
    def test_suggest_name_bad_chars(self):
        parent = self._cut()
        obj = self._cut(title="%'^.j")
        self.assertEqual(obj.suggest_name(parent), 'j')

    def test_suggest_name_bad_chars_too_short(self):
        parent = self._cut()
        obj = self._cut(title="%'^.")
        self.assertRaises(ValueError, obj.suggest_name, parent)

    def test_suggest_name_too_few_chars(self):
        parent = self._cut()
        obj = self._cut(title="")
        self.assertRaises(ValueError, obj.suggest_name, parent)
    
    def test_suggest_name_occupied_namespace(self):
        parent = self._cut()
        parent['a'] = self._cut()
        parent['a-1'] = self._cut()
        parent['a-2'] = self._cut()
        obj = self._cut(title="a")
        self.assertEqual(obj.suggest_name(parent), 'a-3')

    def test_suggest_name_full_namespace(self):
        parent = {}
        parent['a'] = object()
        for i in range(101):
            k = "a-%s" % i
            parent[k] = object()
        obj = self._cut(title='a')
        self.assertRaises(KeyError, obj.suggest_name, parent)

    def test_mark_modified(self):
        obj = self._cut()
        modified = obj.modified
        obj.mark_modified()
        self.failUnless(modified < obj.modified)

    def test_get_field_value_nonexistent_field(self):
        marker = object()
        obj = self._cut()
        self.assertEqual(obj.get_field_value('i_dont_exist', marker), marker)

    def test_get_field_value_normal_field(self):
        obj = self._cut(title='Hello world')
        self.assertEqual(obj.get_field_value('title'), 'Hello world')

    def test_get_field_value_custom_accessor(self):
        class _CustomCls(self._cut):
            custom_accessors = {'title':'_custom_title'}
            def _custom_title(self, default, key=None):
                return "I'm very custom"
            
        obj = _CustomCls(title='Hello world')
        self.assertEqual(obj.get_field_value('title'), "I'm very custom")

    def test_set_field_value_normal_field(self):
        obj = self._cut()
        first = "Hello World"
        second = {'i':1}
        third = object()
        
        obj.set_field_value('first', first)
        obj.set_field_value('second', second)
        obj.set_field_value('third', third)
        
        self.assertEqual(obj.get_field_value('first', first), first)
        self.assertEqual(obj.get_field_value('second', second), second)
        self.assertEqual(obj.get_field_value('third', third), third)

    def test_set_field_value_custom_mutator(self):
        class _CustomCls(self._cut):
            custom_mutators = {'title':'_custom_title'}
            def _custom_title(self, value, key=None):
                self._field_storage['title'] = "I set another title!"

        obj = _CustomCls()
        obj.set_field_value('title', "I am a normal title")
        self.assertEqual(obj.get_field_value('title'), "I set another title!")

    def test_get_field_value_custom_field(self):
        obj = self._custom_versionging_field_fixture()()
        obj.set_field_value('test', 'Hello')
        obj.set_field_value('test', 'World')
        self.assertEqual(obj.get_field_value('test'), 'World')
        field = obj.get_custom_field('test')
        revisions = field.get_revisions()
        self.assertEqual(revisions[1]['value'], 'Hello')        
        self.assertEqual(revisions[2]['value'], 'World')

    def test_get_field_value_versioning_empty(self):
        obj = self._custom_versionging_field_fixture()()
        marker = object()
        self.assertEqual(obj.get_field_value('test', marker), marker)

    def test_nonexistent_custom_field_factory(self):
        class _DummyCls(self._cut):
            custom_fields = {'test':'i_dont_exist'}
        obj = _DummyCls()
        self.assertRaises(ComponentLookupError, obj.set_field_value, 'test', 'hello')
        self.assertRaises(ComponentLookupError, obj.get_field_value, 'test')

    def test_get_custom_field_missing_key_in_custom_fields(self):
        class _DummyCls(self._cut):
            custom_fields = {'hello':'whatever'}        
        obj = _DummyCls()
        self.assertRaises(KeyError, obj.get_custom_field, 'field_404')

    def test_field_appstruct(self):
        obj = self._cut(title="Hello", userid='sven')
        schema = MockSchema()
        res = obj.get_field_appstruct(schema)
        self.failUnless(isinstance(res['created'], datetime))
        self.assertEqual(res['title'], 'Hello')
        self.assertEqual(res['userid'], 'sven')

    def test_field_appstruct_userid_missing_value(self):
        obj = self._cut(title="Hello")
        schema = MockSchema()
        res = obj.get_field_appstruct(schema)
        self.failIf('userid' in res)
        
    def test_set_field_appstruct_some_modified(self):
        obj = self._cut()
        obj.set_field_appstruct({'a':1, 'b':1})
        res = obj.set_field_appstruct({'a':1, 'b':2, 'c':1})
        self.assertEqual(res, set(['b', 'c']))

    def test_set_field_appstruct_notifies_object_updated(self):
        from betahaus.pyracont.interfaces import IObjectUpdatedEvent
        from betahaus.pyracont.interfaces import IBaseFolder
        L = []
        def subscriber(obj, event):
            L.append(event)
        self.config.add_subscriber(subscriber, (IBaseFolder, IObjectUpdatedEvent,))
        obj = self._cut()
        obj.set_field_appstruct({'a':1, 'b':2}, notify=True)
        self.failUnless(IObjectUpdatedEvent.providedBy(L[0]))

    def test_avoid_loops_on_custom_accessors(self):

        class _DummyCls(self._cut):
            """ This class will create a loop, since the custom accessor calls itself
            """
            custom_accessors = {'test':'get_test'}
            def get_test(self, **kwargs):
                return self.get_field_value('test')
        
        obj = _DummyCls()
        self.assertRaises(CustomFunctionLoopError, obj.get_field_value, 'test')

    def test_avoid_loops_on_custom_mutators(self):

        class _DummyCls(self._cut):
            """ This class will create a loop, since the custom mutator calls itself
            """
            custom_mutators = {'test':'set_test'}
            def set_test(self, value, **kwargs):
                return self.set_field_value('test', value)
        
        obj = _DummyCls()
        self.assertRaises(CustomFunctionLoopError, obj.set_field_value, 'test', 'value')

    def test_field_storage(self):
        obj = self._cut()
        self.assertTrue(isinstance(obj.field_storage, OOBTree))
