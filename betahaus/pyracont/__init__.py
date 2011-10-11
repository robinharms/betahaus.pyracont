from uuid import uuid4
from datetime import datetime

import pytz
from slugify import slugify
from zope.component.event import objectEventNotify
from zope.interface import implements
from repoze.folder import Folder
from repoze.folder import unicodify
from BTrees.OOBTree import OOBTree

from betahaus.pyracont.interfaces import IBaseFolder
from betahaus.pyracont.events import ObjectUpdatedEvent
from betahaus.pyracont.factories import createField


class BaseFolder(Folder):
    """ Base class for most content. """
    implements(IBaseFolder)
    schemas = {}
    content_type = 'BaseFolder'
    allowed_contexts = ()
    custom_accessors = {}
    custom_mutators = {}
    custom_fields = {}

    def __init__(self, data=None, **kwargs):
        super(BaseFolder, self).__init__(data=data)
        self.__field_storage__ = OOBTree()
        if 'created' not in kwargs:
            kwargs['created'] = utcnow()
        if 'modified' not in kwargs:
            kwargs['modified'] = kwargs['created']
        if 'uid' not in kwargs:
            kwargs['uid'] = unicode(uuid4())
        self.set_field_appstruct(kwargs, notify=False, mark_modified=True)

    @property
    def title(self):
        return self.get_field_value('title', u'')

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
        return self.__field_storage__

    def suggest_name(self, parent):
        """ Suggest a name if this content would be added to parent.
        """
        title = self.title
        if not title:
            raise ValueError("title property didn't return any text.")
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
        if key in self.custom_fields:
            field = self.get_custom_field(key)
            return field.get(default=default)
        return self._field_storage.get(key, default)

    def set_field_value(self, key, value, override=False):
        """ Set field value.
            Will not send events, so use this if you silently want to change a single field.
            You can override field behaviour by either setting custom mutators
            or make a field a custom field.
            override bypasses any custom mutators. Good idea if you're calling from a custom mutator.
        """
        if not override and key in self.custom_mutators:
            mutator = self.custom_mutators[key]
            if isinstance(mutator, basestring):
                mutator = getattr(self, mutator)
            mutator(value, key=key)
            return
        if not override and key in self.custom_fields:
            field = self.get_custom_field(key)
            field.set(value)
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

    def get_custom_field(self, key):
        if key not in self.custom_fields:
            raise KeyError("There's no custom field defined in custom_fields with the name '%s'" % key)
        if key not in self._field_storage:
            field_type = self.custom_fields[key]
            field = createField(field_type, key=key)
            self._field_storage[key] = field
        return self._field_storage[key]


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
