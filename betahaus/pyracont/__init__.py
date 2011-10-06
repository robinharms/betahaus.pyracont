from uuid import uuid4
from datetime import datetime

import pytz
from slugify import slugify
from zope.component.event import objectEventNotify
from zope.interface import implements
from repoze.folder import Folder
from repoze.folder import unicodify
from BTrees.OOBTree import OOBTree
from BTrees.LOBTree import LOBTree
from persistent import Persistent
from pyramid.threadlocal import get_current_request
from pyramid.security import authenticated_userid

from betahaus.pyracont.interfaces import IBaseFolder
from betahaus.pyracont.interfaces import IVersioningField
from betahaus.pyracont.events import ObjectUpdatedEvent
from betahaus.pyracont.factories import createContent
from zope.component.interfaces import ComponentLookupError


class BaseFolder(Folder):
    """ Base class for most content. """
    implements(IBaseFolder)
    schemas = {}
    content_type = 'BaseFolder'
    allowed_contexts = ()
    custom_accessors = {}
    custom_mutators = {}
    versioning_fields = ()

    def __init__(self, data=None, **kwargs):
        super(BaseFolder, self).__init__(data=data)
        if 'created' not in kwargs:
            kwargs['created'] = utcnow()
        if 'modified' not in kwargs:
            kwargs['modified'] = kwargs['created']
        if 'uid' not in kwargs:
            kwargs['uid'] = unicode(uuid4())
        self.set_field_appstruct(kwargs, notify=False, mark_modified=True)

    @property
    def title(self):
        return self.get_field_value('title', '')

    @property
    def created(self):
        return self.get_field_value('created')

    @property
    def modified(self):
        return self.get_field_value('modified')

    @property
    def uid(self):
        return self.get_field_value('uid')

    @property
    def _field_storage(self):
        if not hasattr(self, '__field_storage__'):
            self.__field_storage__ = OOBTree()
        return self.__field_storage__

    def suggest_name(self, parent):
        """ Suggest a name if this content would be added to parent.
        """
        title = self.title
        if not title:
            raise ValueError("Title can't be empty to use suggest_name")
        return generate_slug(parent, title)

    def mark_modified(self):
        """ Mark content as modified. """
        self._field_storage['modified'] = utcnow()

    def get_field_value(self, key, default=None):
        """ Return field value, or default """
        if key in self.custom_accessors:
            accessor = self.custom_accessors[key]
            if isinstance(accessor, basestring):
                accessor = getattr(self, accessor)
            return accessor(default=default, key=key)
        if key in self.versioning_fields:
            return self._get_versioning_field_value(key, default=default)
        return self._field_storage.get(key, default)

    def set_field_value(self, key, value):
        """ Set field value.
            Will not send events, so use this if you silently want to change a single field.
            You can override field behaviour by either setting custom mutators
            or make a field a versioning field.
        """
        if key in self.custom_mutators:
            mutator = self.custom_mutators[key]
            if isinstance(mutator, basestring):
                mutator = getattr(self, mutator)
            mutator(value, key=key)
            return
        if key in self.versioning_fields:
            self._set_versioning_field_value(key, value)
            return
        self._field_storage[key] = value

    def get_field_appstruct(self, schema):
        """ Return a dict of all fields and their values.
            Deform expects input like this when rendering already saved values.
        """
        marker = object()
        appstruct = {}
        for field in schema:
            value = self.get_field_value(field.name, marker)
            if value != marker:
                appstruct[field.name] = value
        return appstruct

    def set_field_appstruct(self, values, notify=True, mark_modified=True):
        """ Set values from a dict or similar key/value object.
            Only updates if the new value isn't the same as the old one.
            Returns set of keys (fieldnames) that have been updated.
        """
        updated = set()
        for (k, v) in values.items():
            cur = self.get_field_value(k)
            if cur == v:
                continue
            self.set_field_value(k, v)
            updated.add(k)
        if updated:
            if notify:
                objectEventNotify(ObjectUpdatedEvent(self, fields=updated))
            if mark_modified and 'modified' not in values:
                #Don't update if modified is set, since it will override the value we're trying to set.
                self.mark_modified()
        return updated

    def get_versioning_field(self, key):
        """ Return versioning field. Create it if it doesn't exist. """
        if key not in self.versioning_fields:
            raise KeyError("There's no versioning field called '%s'" % key)
        if key not in self._field_storage:
            try:
                field = createContent('VersioningField')
            except ComponentLookupError:
                field = VersioningField()
            self._field_storage[key] = field
        return self._field_storage[key]

    def _get_versioning_field_value(self, key, default=None):
        field = self.get_versioning_field(key)
        value = field.get_last_revision_value(default=default)
        if value == default:
            return default
        return value

    def _set_versioning_field_value(self, key, value):
        field = self.get_versioning_field(key)
        field.add(value)


class VersioningField(Persistent):
    """ Field that has versioning rather than just storing one value. """
    implements(IVersioningField)

    def __init__(self):
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
            author = authenticated_userid(request)
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

    def get_last_revision_value(self, default=None):
        if not len(self._revision_values):
            return default
        id = self.get_current_rev_id()
        return self._revision_values[id]

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


def utcnow():
    """Get the current datetime localized to UTC.

    The difference between this method and datetime.utcnow() is
    that datetime.utcnow() returns the current UTC time but as a naive
    datetime object, whereas this one includes the UTC tz info."""

    naive_utcnow = datetime.utcnow()
    return pytz.utc.localize(naive_utcnow)


def generate_slug(parent, text, limit=20):
    """ Suggest a name for content that will be added.
        text is a title or similar to be used.
    """
    text = unicodify(text)
    suggestion = slugify(text[:limit])
    if not len(suggestion):
        raise ValueError("When text was made URL-friendly, nothing remained.")

    #Is the suggested ID already unique?
    if suggestion not in parent:
        return suggestion
    
    #ID isn't unique, let's try to generate a unique one.
    RETRY = 100
    i = 1
    while i <= RETRY:
        new_s = "%s-%s" % (suggestion, str(i))
        if new_s not in parent:
            return new_s
        i += 1
    #If no id was found, don't just continue
    raise KeyError("No unique id could be found")
