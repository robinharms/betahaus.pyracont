from unittest import TestCase

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass


class VersioningFieldTests(TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont.fields.versioning import VersioningField
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

    def test_set(self):
        """ Set is almost same as add. Important for compatibility when field is not directly accessed. """
        obj = self._cut()
        obj.set('hello')
        self.assertEqual(obj.get(), 'hello')

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

    def test_get(self):
        now = self._now()
        obj = self._cut()
        obj.add('Hello')
        obj.add('World')
        obj.add('!', author='hi', created=now)
        self.assertEqual(obj.get(), '!')

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
