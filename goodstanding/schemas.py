import colander

class gsClassSchema(colander.MappingSchema):
    classCode = colander.SchemaNode(colander.String())
    cohort = colander.SchemaNode(colander.Integer())

