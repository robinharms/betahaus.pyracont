from unittest import TestCase

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass

from betahaus.pyracont.interfaces import ILangField
from betahaus.pyracont.interfaces import IFieldFactory

class LangFieldTests(TestCase):
    def setUp(self):
        self.config = testing.setUp(request = testing.DummyRequest())

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from betahaus.pyracont.fields.lang import LangField
        return LangField

    def test_verify_class(self):
        self.failUnless(verifyClass(ILangField, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(ILangField, self._cut()))

    def test_langs(self):
        obj = self._cut()
        obj.__data__['sv'] = 'Hej'
        obj.__data__['en'] = 'Hello'
        self.assertEqual(obj.langs, set(['sv', 'en']))

    def test_translated(self):
        obj = self._cut()
        obj.__data__['sv'] = 'Hej'
        obj.__data__['en'] = 'Hello'
        #English is default
        self.assertEqual(obj.translated, set(['sv']))

    def test_get_without_anything_set(self):
        default = object()
        obj = self._cut()
        self.assertEqual(obj.get(default), {'en': default})

    def test_get_without_request_set_and_no_lang_specified(self):
        obj = self._cut()
        obj.__data__['en'] = 'Blabla'
        self.assertEqual(obj.get(), {'en': 'Blabla'})

    def test_get_with_nonexistent_languages(self):
        default = object()
        obj = self._cut()
        obj.__data__['en'] = 'Blabla'
        self.assertEqual(obj.get(default = default, langs = ['hi', 'en']), {'en': 'Blabla', 'hi': default})

    def test_set_main(self):
        obj = self._cut()
        obj.set({'en': 'Hello'})
        self.assertEqual(len(obj.fuzzy), 0)
        self.assertEqual(obj.__data__['en'], 'Hello')

    def test_set_main_marks_others_fuzzy(self):
        obj = self._cut()
        obj.set({'sv': 'Hej'})
        obj.set({'en': 'Hello there'})
        self.assertIn('sv', obj.fuzzy)

    def test_set_single_unmarks_fuzzy(self):
        obj = self._cut()
        obj.fuzzy.add('sv')
        obj.set({'sv': 'Hej'})
        self.assertEqual(len(obj.fuzzy), 0)

    def test_set_both_doesnt_mark_as_fuzzy(self):
        obj = self._cut()
        obj.set({'sv': 'Hej', 'en': 'Hello'})
        self.assertEqual(len(obj.fuzzy), 0)

    def test_set_with_bad_value(self):
        obj = self._cut()
        self.assertRaises(TypeError, obj.set, 'Hello')

    def test_remove(self):
        obj = self._cut()
        obj.set({'hi': 'boo'})
        obj.set({'sv': 'Hej', 'en': 'Hello'})
        obj.remove('sv')
        obj.remove('hi')
        self.assertEqual(len(obj.fuzzy), 0)
        self.assertNotIn('sv', obj.langs)


    def test_len(self):
        obj = self._cut()
        obj.set({'hi': 'boo'})
        obj.set({'sv': 'Hej', 'en': 'Hello'})
        self.assertEqual(len(obj), 3)

    def test_integration(self):
        self.config.include('betahaus.pyracont.fields.lang')
        self.failUnless(self.config.registry.queryUtility(IFieldFactory, name = 'LangField'))
