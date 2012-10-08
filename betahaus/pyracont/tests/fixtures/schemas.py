import colander

from betahaus.pyracont.decorators import schema_factory


@schema_factory('DummySchema', title=u"dummy schema title", description=u"dummy schema description")
class DummySchema(colander.Schema):
    dummy_schema_node = colander.SchemaNode(colander.String(),
                                            transform_out = 'transform_out',
                                            transform_in = 'transform_in',)


class Phone(colander.Schema):
    number = colander.SchemaNode(colander.String(),
                                 transform_out = 'transform_out',
                                 transform_in = 'transform_in',)

class Contacts(colander.SequenceSchema):
    phone_nos = Phone()

class Person(colander.Schema):
    name = colander.SchemaNode(colander.String(),
                               transform_out = 'transform_out',
                               transform_in = 'transform_in',)
    contacts = Contacts()

class People(colander.SequenceSchema):
    person = Person()

@schema_factory('DummyPeopleSchema')
class DummyPeopleSchema(colander.Schema):
    people = People()

