from marshmallow import Schema, fields
from .common import PaginationSchema


class JokeListQueryArgs(PaginationSchema):
    # All optional filters (query string)
    age_group = fields.String(load_default=None)
    era = fields.String(load_default=None)
    region = fields.String(load_default=None)
    acceptability = fields.String(load_default=None)
    delivery_type = fields.String(load_default=None)
    q = fields.String(load_default=None)   # text search
