from marshmallow import Schema, fields, validate


class JokeCreateSchema(Schema):
    """Schema for creating a new joke."""
    
    text_tn = fields.String(required=True, validate=validate.Length(min=1))
    text_fr = fields.String(allow_none=True)
    text_en = fields.String(allow_none=True)
    
    age_group = fields.String(allow_none=True)
    era = fields.String(allow_none=True)
    region = fields.String(allow_none=True)
    acceptability = fields.String(allow_none=True)
    delivery_type = fields.String(allow_none=True)
    
    tone = fields.String(allow_none=True)
    rhythm = fields.String(allow_none=True)
    
    is_published = fields.Boolean(load_default=False)


class JokeUpdateSchema(Schema):
    """Schema for updating a joke."""
    
    text_tn = fields.String(allow_none=True)
    text_fr = fields.String(allow_none=True)
    text_en = fields.String(allow_none=True)
    
    age_group = fields.String(allow_none=True)
    era = fields.String(allow_none=True)
    region = fields.String(allow_none=True)
    acceptability = fields.String(allow_none=True)
    delivery_type = fields.String(allow_none=True)
    
    tone = fields.String(allow_none=True)
    rhythm = fields.String(allow_none=True)
    
    is_published = fields.Boolean(allow_none=True)


class JokeSchema(Schema):
    id = fields.Int(dump_only=True)
    text_tn = fields.Str(required=True)
    text_fr = fields.Str()
    text_en = fields.Str()
    age_group = fields.Str()
    era = fields.Str()
    region = fields.Str()
    acceptability = fields.Str()
    delivery_type = fields.Str()
    tone = fields.Str()
    rhythm = fields.Str()
    is_published = fields.Bool()
    author_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()



class JokeListQueryArgsSchema(Schema):
    """Schema for query parameters when listing jokes."""
    
    page = fields.Integer(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Integer(load_default=20, validate=validate.Range(min=1, max=100))
    
    # Filters
    age_group = fields.String(allow_none=True)
    era = fields.String(allow_none=True)
    region = fields.String(allow_none=True)
    acceptability = fields.String(allow_none=True)
    delivery_type = fields.String(allow_none=True)
    
    # Search
    q = fields.String(allow_none=True)  # Full text search


class JokeListResponseSchema(Schema):
    page = fields.Int()
    per_page = fields.Int()
    total = fields.Int()
    items = fields.List(fields.Nested(JokeSchema))
