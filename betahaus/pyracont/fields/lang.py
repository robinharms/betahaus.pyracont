from BTrees.OOBTree import OOSet
from BTrees.OOBTree import OOBTree
from pyramid.threadlocal import get_current_request
from pyramid.i18n import get_locale_name
from zope.interface import implementer

from betahaus.pyracont.fields.base import BaseField
from betahaus.pyracont.interfaces import ILangField
from betahaus.pyracont.decorators import field_factory


@field_factory('LangField')
@implementer(ILangField)
class LangField(BaseField):
    """ Language sensitive field. """

    def __init__(self, key=None, main_lang = None, **kwargs):
        super(LangField, self).__init__(key=key, **kwargs)
        if not main_lang:
            request = get_current_request()
            main_lang = request.registry.settings.get('default_locale_name', 'en')
        self.main_lang = main_lang
        self.fuzzy = OOSet()
        self.__data__ = OOBTree()

    @property
    def langs(self):
        return set(self.__data__.keys())

    @property
    def translated(self):
        return self.langs - set([self.main_lang])

    def get(self, default=None, langs = None, **kwargs):
        if not langs:
            request = get_current_request()
            langs = (get_locale_name(request),)
        return dict((lang, self.__data__.get(lang, default)) for lang in langs)

    def set(self, value, **kwargs):
        if not isinstance(value, dict):
            raise TypeError("Must be a dict")
        updated = value.keys()
        main_updated = self.main_lang in updated
        for (lang, value) in value.items():
            self.__data__[lang] = value
            if lang in self.fuzzy:
                self.fuzzy.remove(lang)
        if main_updated:
            others = self.translated - set(updated)
            self.fuzzy.update(others)

    def remove(self, key):
        self.__data__.pop(key, None)
        if key in self.fuzzy:
            self.fuzzy.remove(key)

    def __len__(self):
        return len(self.__data__)


def includeme(config):
    config.scan(__name__)
