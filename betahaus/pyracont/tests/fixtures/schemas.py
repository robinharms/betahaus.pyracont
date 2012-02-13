import colander

from betahaus.pyracont.decorators import schema_factory


@schema_factory('DummySchema', title=u"dummy schema title", description=u"dummy schema description")
class DummySchema(colander.Schema):
    dummy_schema_node = colander.SchemaNode(colander.String())
