from zope.component.interfaces import IFactory
from zope.interface import Attribute
from zope.interface import Interface


class IContentFactory(IFactory):
    """ Factory for persistent objects / content types. Works the same way as IFactory """
    

class ISchemaFactory(IFactory):
    """ Factory for colander.Schema objects. Works the same way as IFactory """


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
    versioning_fields = Attribute(
        " A list of fields where they should employ versioning rather than just storing a value.")

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
            - Check if the field is a versioning field.
            - Retrieve data from normal storage and return.
        """
    
    def set_field_value(key, value):
        """ Set field value.
            Will not send events, so use this if you silently want to change a single field.
            You can override field behaviour by either setting custom mutators
            or make a field a versioning field. It has the same priority and orders as get_field_value
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

    def get_versioning_field(key):
        """ Return versioning field. Create it if it doesn't exist.
            Will only work if key is specified in versioning_fields attribute.
        """

