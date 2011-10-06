import colander

from betahaus.pyracont.decorators import schema_factory


@schema_factory('DummySchema')
class OtherSchema(colander.Schema):
    other_schema_node = colander.SchemaNode(colander.String())
