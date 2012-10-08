import colander

from betahaus.pyracont.decorators import schema_factory


class Tag(colander.Schema):
    title = colander.SchemaNode(colander.String())


class Tags(colander.SequenceSchema):
    tag = Tag()


@schema_factory('ContentSchema')
class ContentSchema(colander.Schema):
    title = colander.SchemaNode(colander.String())
    tags = Tags()
    text = colander.SchemaNode(colander.String(),
                               transform_in = 'text_input',
                               transform_out = 'text_output')
