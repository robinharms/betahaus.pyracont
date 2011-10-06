from unittest import TestCase
from datetime import datetime

import colander
from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass


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

    def test_get_and_set_field_value_versioning_field(self):
        self.config.scan('betahaus.pyracont')
        class _CustomCls(self._cut):
            versioning_fields = ('test',)

        obj = _CustomCls()
        obj.set_field_value('test', 'Hello')
        obj.set_field_value('test', 'World')
        field = obj.get_versioning_field('test')
        revisions = field.get_revisions()
        self.assertEqual(revisions[1]['value'], 'Hello')        
        self.assertEqual(revisions[2]['value'], 'World')        

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

    def test_get_versioning_field(self):
        from betahaus.pyracont import VersioningField
        self.config.scan('betahaus.pyracont')

        class _CustomCls(self._cut):
            versioning_fields = ('test',)

        obj = _CustomCls()
        field = obj.get_versioning_field('test')
        self.failUnless(isinstance(field, VersioningField))

    def test_get_versioning_field_nonexistent_field(self):
        obj = self._cut()
        self.assertRaises(KeyError, obj.get_versioning_field, "i_dont_exist")


class VersioningFieldTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont import VersioningField
        return VersioningField

    def _now(self):
        from betahaus.pyracont import utcnow
        return utcnow()

    def test_verify_class(self):
        from betahaus.pyracont.interfaces import IVersioningField
        self.failUnless(verifyClass(IVersioningField, self._cut))

    def test_verify_obj(self):
        from betahaus.pyracont.interfaces import IVersioningField
        self.failUnless(verifyObject(IVersioningField, self._cut()))

    def test_get_current_rev_id(self):
        obj = self._cut()
        self.assertEqual(obj.get_current_rev_id(), 0)
        obj.add('Hello')
        self.assertEqual(obj.get_current_rev_id(), 1)

    def test_add(self):
        obj = self._cut()
        now = self._now()
        obj.add('Hello', author='some_user', created=now)
        self.assertEqual(obj._revision_values[1], 'Hello')
        self.assertEqual(obj._revision_authors[1], 'some_user')
        self.assertEqual(obj._revision_created_timestamps[1], now)

    def test_add_lookup_userid(self):
        self.config.testing_securitypolicy(userid='tester')
        obj = self._cut()
        obj.add('Something')
        rev = obj.get_last_revision()
        self.assertEqual(rev['author'], 'tester')

    def test_remove(self):
        obj = self._cut()
        obj.add('Hello')
        obj.add('World')
        obj.add('!')
        self.assertEqual(len(obj), 3)
        obj.remove(2)
        self.assertEqual(len(obj), 2)

    def test_get_last_revision(self):
        now = self._now()
        obj = self._cut()
        obj.add('Hello')
        obj.add('World')
        obj.add('!', author='hi', created=now)
        res = obj.get_last_revision()
        self.assertEqual(res, {'value':'!', 'author': 'hi', 'created': now})

    def test_get_last_revision_no_existing_revisions(self):
        obj = self._cut()
        marker = object()
        res = obj.get_last_revision(marker)
        self.assertEqual(res, marker)


    def test_get_last_revision_value(self):
        now = self._now()
        obj = self._cut()
        obj.add('Hello')
        obj.add('World')
        obj.add('!', author='hi', created=now)
        self.assertEqual(obj.get_last_revision_value(), '!')


    def test_get_revision(self):
        now = self._now()
        obj = self._cut()
        obj.add('Hello', author='one', created=now)
        obj.add('World', author='two', created=now)
        obj.add('!', author='three', created=now)
        res1 = obj.get_revision(1)
        self.assertEqual(res1, {'value':'Hello', 'author': 'one', 'created': now})
        res2 = obj.get_revision(2)
        self.assertEqual(res2, {'value':'World', 'author': 'two', 'created': now})

    def test_get_revision_nonexistent_key(self):
        obj = self._cut()
        self.assertRaises(KeyError, obj.get_revision, 1)

    def test_get_revisions(self):
        now = self._now()
        obj = self._cut()
        obj.add('Hello', author='one', created=now)
        obj.add('World', author='two', created=now)
        obj.add('!', author='three', created=now)
        res = obj.get_revisions()
        expected = {}
        expected[1] = {'value':'Hello', 'author': 'one', 'created': now}
        expected[2] = {'value':'World', 'author': 'two', 'created': now}
        expected[3] = {'value':'!', 'author': 'three', 'created': now}
        self.assertEqual(res, expected)


class DecoratorsTests(TestCase):
    #FIXME
    pass


class EventsTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont.events import ObjectUpdatedEvent
        return ObjectUpdatedEvent

    def test_verify_class(self):
        from betahaus.pyracont.interfaces import IObjectUpdatedEvent
        self.failUnless(verifyClass(IObjectUpdatedEvent, self._cut))

    def test_verify_obj(self):
        from betahaus.pyracont.interfaces import IObjectUpdatedEvent
        self.failUnless(verifyObject(IObjectUpdatedEvent, self._cut(object())))


class FactoriesTests(TestCase):
    #FIXME
    pass


