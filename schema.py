from marshmallow import Schema, fields


class CompanySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    address = fields.Str(required=True)
    owner = fields.Str(required=True)


class UpdateCompanySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    address = fields.Str()
    owner = fields.Str()


class UserRegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)


class UpdateUserRegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()
    username = fields.Str()


class UpdatePasswordSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class UserLoginSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
