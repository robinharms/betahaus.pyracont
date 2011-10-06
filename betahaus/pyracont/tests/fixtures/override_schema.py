import colander

from betahaus.pyracont.decorators import schema_factory


@schema_factory('DummySchema')
class OtherSchema(colander.Schema):
    pass