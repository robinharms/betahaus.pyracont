from datetime import datetime

from BTrees.LOBTree import LOBTree
from pyramid.threadlocal import get_current_request
from zope.interface import implementer

from betahaus.pyracont.fields.base import BaseField
from betahaus.pyracont.interfaces import IVersioningField
from betahaus.pyracont.decorators import field_factory
from betahaus.pyracont import utcnow


@field_factory('VersioningField')
@implementer(IVersioningField)
class VersioningField(BaseField):
    """ Field that has versioning rather than just storing one value. """

    def __init__(self, key=None, **kwargs):
        super(VersioningField, self).__init__(key=key, **kwargs)
        self.__revision_values__ = LOBTree()
        self.__revision_authors__ = LOBTree()
        self.__revision_created_timestamps__ = LOBTree()

    @property
    def _revision_values(self):
        return self.__revision_values__
    
    @property
    def _revision_authors(self):
        return self.__revision_authors__

    @property
    def _revision_created_timestamps(self):
        return self.__revision_created_timestamps__

    def get(self, default=None, **kwargs):
        """ Return value of last revision """
        if not len(self._revision_values):
            return default
        id = self.get_current_rev_id()
        return self._revision_values[id]

    def set(self, value, **kwargs):
        self.add(value)

    def get_current_rev_id(self):
        if len(self._revision_values) == 0:
            return 0
        return self._revision_values.maxKey()

    def add(self, value, author=None, created=None):
        if created is None:
            created = utcnow()
        assert isinstance(created, datetime)
        if author is None:
            request = get_current_request()
            author = request.authenticated_userid
        #author might still be None, if this is run by a script or by an unauthenticated user
        id = self.get_current_rev_id()+1
        self._revision_values[id] = value
        self._revision_authors[id] = author
        self._revision_created_timestamps[id] = created
    
    def remove(self, id):
        del self._revision_values[id]
        del self._revision_authors[id]
        del self._revision_created_timestamps[id]

    def get_last_revision(self, default=None):
        if not len(self._revision_values):
            return default
        id = self.get_current_rev_id()
        return self.get_revision(id)

    def get_revision(self, id):
        result = {}
        result['value'] = self._revision_values[id]
        result['author'] = self._revision_authors[id]
        result['created'] = self._revision_created_timestamps[id]
        return result

    def get_revisions(self):
        results = {}
        for k in self._revision_values:
            rev = {}
            rev['value'] = self._revision_values[k]
            rev['author'] = self._revision_authors[k]
            rev['created'] = self._revision_created_timestamps[k]
            results[k] = rev
        return results

    def __len__(self):
        return len(self._revision_values)


def includeme(config):
    config.scan(__name__)
