from zope.component.interfaces import IFactory
from zope.interface import Attribute
from zope.interface import Interface


class IContentFactory(IFactory):
    """ Factory for persistent objects / content types. Works the same way as IFactory """
    

class ISchemaFactory(IFactory):
    """ Factory for colander.Schema objects. Requires context and request to work.
        Will return a bound schema instance.
    """


class IFieldFactory(IFactory):
    """ Factory for fields. Works the same way as IFactory. """


class IObjectUpdatedEvent(Interface):
    """ Event sent when fields have been updated. """
    object = Attribute("The object this event is for.")
    fields = Attribute("Fields that have been updated."
                       "Should be a list with regular strings that correspond to field keys.")
    
    def __init__(object, fields=(),):
        """ Init event. Usuallu done like this: 
            >>> from zope.component.event import objectEventNotify
            >>> context = SomeClass()
            >>> event = ObjectUpdatedEvent(context, fields=('updated', 'fields')
            >>> objectEventNotify(event)
        """
    

class IBaseFolder(Interface):
    """ Base content type for all regular persistent models."""
    title = Attribute("Title")
    created = Attribute(
        "A TZ-aware datetime.datetime of when this was created in UTC time.")
    modified = Attribute(
        "A TZ-aware datetime.datetime of when this was updated last in UTC time.")
    uid = Attribute("Unique ID")

    schemas = Attribute(
        """ Dict that contains a mapping for action -> schema factory name.
            Example:{'edit':'site_root_edit_schema'}.""")

    allowed_contexts = Attribute(
        " List of which contexts this content is allowed in. Should correspond to content_type")

    content_type = Attribute("The id of this content type.")

    custom_accessors = Attribute(
        """ Dict of custom accessors to use. The key is which field to override,
            value should be a string which represent a callable on this class, or a callable method.
            The accessor method must accept default and key as kwarg.""")

    custom_mutators = Attribute(
        """ Same as custon accessor, but the callable must accept a value.
            The mutator method must accept value as argument.
            Method must also accept key as kwarg.""")

    custom_fields = Attribute(
        """ A dict of fields consisting of key (field name) and field factory name.
            A field type must be registered with that factory name.
            Example: {'wiki_text':'VersioningField'} if your register a field factory
            with the name 'VersioningField'.""")

    field_storage = Attribute(
        """ An OOBTree storage for field values. The point of exposing this
            is to enable bypass of custom mutators or accessors.""")

    def __init__(data=None, **kwargs):
        """ Init class. Any kwargs passed will be stored in this content. """

    def suggest_name(parent):
        """ Suggest a name if this content would be added to parent.
        """

    def mark_modified():
        """ Set this content as modified. Will bypass custom mutators to avoid loops.
            The only way to customise this is to override it.
            Only set_field_appstruct will trigger this method.
            If you set a field any other way, you'll have to trigger it manually.
        """

    def get_field_value(key, default=None):
        """ Return field value, or default.
            The lookup order is as follows:
            - Check if there's a custom accessor.
            - Check if the field is a custom field.
            - Retrieve data from normal storage and return.
        """
    
    def set_field_value(key, value):
        """ Set field value.
            Will not send events, so use this if you silently want to change a single field.
            You can override field behaviour by either setting custom mutators
            or make a field a custom field.
        """

    def get_field_appstruct(schema):
        """ Return a dict of all fields and their values.
            Deform expects input like this when rendering already saved values.
            Versioning fields will be represented with their current value.
        """

    def set_field_appstruct(values, notify=True, mark_modified=True):
        """ Set values from a dict or similar key/value object.
            Only updates if the new value isn't the same as the old one.
            Returns set of keys (fieldnames) that have been updated.
            notify: Send notification
            mark_modified: mark content as updated if anything was changed.
        """

    def get_custom_field(key):
        """ Return custom field. Create it if it doesn't exist.
            Will only work if key:field_type is specified in custom_fields attribute.
        """


class IBaseField(Interface):
    """ """
    key = Attribute("Store which key this field will be accessed by. For convenience.")
    
    def __init__(key=None, **kwargs):
        """ Initialize field. key is the key of the field,
            same as the value that will be passed to get_field_value method.
        """

    def get(default=None):
        """ Get field value """
    
    def set(value):
        """ Set field value """


class IVersioningField(IBaseField):
    """ Versioning fields store a value like any other, but they also keep the
        old values and keep track of author and when each revision was added.
    """

    def get_current_rev_id():
        """ Return current revision id, always an integer.
            0 if no revisions exist.
        """

    def add(value, author=None, created=None):
        """ Add a new revision.
            author: Author of this revision. If it's None, the field will try to extract it from the current request.
            created: TZ-aware datetime of when it was created. Will set now in UTC timezone if it's None.
        """

    def remove(id):
        """ Remove a revision completely. Normally a bad idea to use,
            since it goes against the purpouse of versioning.
        """

    def get_last_revision(default=None):
        """ Return last revision, or default if no revision exist.
            Will get full revision info with a dict containing author, value and created.
        """

    def get_revision(id):
        """ Get a specific revision.
        """

    def get_revisions():
        """ Return a dict of all revisions with revision number as key, and value will be each revisions info.
            Example: {1:{'value':'Hello', 'author':'some_userid', 'created':'<datetime>'}, 2:{<etc...>}}
        """


class IPasswordField(IBaseField):
    """ Stores SHA1-value (as default) instead of plaintext. """

    min_length = Attribute("Min length of password. Default 5")
    hash_method = Attribute("Callable method to hash passwords with. Defaults to SHA1. Custom method must accept a single value.")


    def get(default=None):
        """ Get hashed value or default if field is set as None. """

    def set(value):
        """ Hash value and store it. """

    def check_input(value):
        """ Accepts plaintext, uses hash_method on it an compares the result.
            Will always be False if password isn't set.
        """

    def clear_password():
        """ Removes stored password and set the field as None.
        """
