import colander
from zope.interface import Interface

from betahaus.pyracont.decorators import schema_factory


class IDummySchema(Interface):
    pass


@schema_factory('DummySchema', title=u"dummy schema title", description=u"dummy schema description", provides = IDummySchema)
class DummySchema(colander.Schema):
    dummy_schema_node = colander.SchemaNode(colander.String(),)


class Phone(colander.Schema):
    number = colander.SchemaNode(colander.String(),)

class Contacts(colander.SequenceSchema):
    phone_nos = Phone()


class Person(colander.Schema):
    name = colander.SchemaNode(colander.String(),)
    contacts = Contacts()


class People(colander.SequenceSchema):
    person = Person()


@schema_factory('DummyPeopleSchema')
class DummyPeopleSchema(colander.Schema):
    people = People()

