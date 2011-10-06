import colander

from betahaus.pyracont.decorators import schema_factory


@schema_factory('DummySchema')
class DummySchema(colander.Schema):
    title = colander.SchemaNode(colander.String())