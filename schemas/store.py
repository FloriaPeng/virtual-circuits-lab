from ma import ma
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)
    # tell the marshmallow that the items is nested in store (store contains many items)
    # marshmallow then knows that this is not something to load, but something to dump

    class Meta:
        model = StoreModel
        dump_only = ("id",)
        include_fk = True  # include foreign key in dump (it is not going to be loaded by any means)
        load_instance = True
