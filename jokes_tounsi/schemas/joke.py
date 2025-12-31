from marshmallow import Schema, fields, validate
from ..utils.constants import (
    AGE_GROUPS,
    ERAS,
    REGIONS,
    ACCEPTABILITY_LEVELS,
    DELIVERY_TYPES,
)



class JokeBaseSchema(Schema):
    text_tn = fields.String(required=True, validate=validate.Length(min=1))
    text_fr = fields.String(load_default=None)
    text_en = fields.String(load_default=None)

    age_group = fields.String(
        load_default=None,
        validate=validate.OneOf(AGE_GROUPS),
    )
    era = fields.String(
        load_default=None,
        validate=validate.OneOf(ERAS),
    )
    region = fields.String(
        load_default=None,
        validate=validate.OneOf(REGIONS),
    )
    acceptability = fields.String(
        load_default=None,
        validate=validate.OneOf(ACCEPTABILITY_LEVELS),
    )
    delivery_type = fields.String(
        load_default=None,
        validate=validate.OneOf(DELIVERY_TYPES),
    )

    tone = fields.String(load_default=None)
    rhythm = fields.String(load_default=None)


class JokeCreateSchema(JokeBaseSchema):
    """Schema used when creating a joke."""
    is_published = fields.Boolean(load_default=False)


class JokeSchema(JokeBaseSchema):
    """Schema used when returning jokes to clients."""
    id = fields.Int(dump_only=True)
    is_published = fields.Boolean()
    created_at = fields.DateTime()
