from marshmallow import Schema, fields as MarshmallowFields

class UserSchema(Schema):
    id = MarshmallowFields.Str()
    name = MarshmallowFields.Str()
    username = MarshmallowFields.Str()
    email = MarshmallowFields.Str()
    city = MarshmallowFields.Str()
    province =  MarshmallowFields.Str()
    country = MarshmallowFields.Str()
    address = MarshmallowFields.Str()
    zip_code = MarshmallowFields.Str()
    phone = MarshmallowFields.Str()


class OrderSchema(Schema):
    id = MarshmallowFields.Str()
    user = MarshmallowFields.Str()
    order_date = MarshmallowFields.DateTime()


class ProductSchema(Schema):
    id = MarshmallowFields.Str()
    name = MarshmallowFields.Str()
    sku = MarshmallowFields.Str()
    price = MarshmallowFields.Float()
    image_url = MarshmallowFields.Str()
    description = MarshmallowFields.Str()

class OrderDetailSchema(Schema):
    id = MarshmallowFields.Str()
    order = MarshmallowFields.Str()
    product = MarshmallowFields.Str()
    quantity = MarshmallowFields.Integer()
    total_price = MarshmallowFields.Float()