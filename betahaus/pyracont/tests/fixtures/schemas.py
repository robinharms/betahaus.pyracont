import colander

from betahaus.pyracont.decorators import schema_factory


@schema_factory('DummySchema')
class DummySchema(colander.Schema):
    dummy_schema_node = colander.SchemaNode(colander.String())
