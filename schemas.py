from marshmallow import Schema, fields

class PlainReligionSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    
class PlainMaritalStatusSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    
class PlainEmployeeSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    user_name = fields.Str(required=True)
    phone = fields.Str(required=True)
    dob = fields.Str(required=True)
    address_perm = fields.Str(required=True)
    address_curr = fields.Str(required=True)

class EmployeeUpdateSchema(Schema):
    name = fields.Str()
    user_name = fields.Str()
    phone = fields.Str()
    dob = fields.Str()
    address_perm = fields.Str()
    address_curr = fields.Str()
    
    religion_id = fields.Int()
    marital_status_id = fields.Int()
    
class ReligionSchema(PlainReligionSchema):
    employees = fields.List(fields.Nested(PlainEmployeeSchema), dump_only = True)

class MaritalStatusSchema(PlainMaritalStatusSchema):
    employees = fields.List(fields.Nested(PlainEmployeeSchema), dump_only = True)

class EmployeeSchema(PlainEmployeeSchema):
    religion_id = fields.Int(required=True, load_only = True)
    religion = fields.Nested(PlainReligionSchema(), dump_only = True)
    
    marital_status_id = fields.Int(required=True, load_only = True)
    marital_status = fields.Nested(PlainMaritalStatusSchema(), dump_only = True)

class PlainDepartmentSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)

class PlainOfficePostSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    parent_id = fields.Integer(required=True)
    
class DepartmentSchema(PlainDepartmentSchema):
    office_posts = fields.List(fields.Nested(PlainOfficePostSchema()), dump_only = True)
    
class OfficePostSchema(PlainOfficePostSchema):
    department_id = fields.Int(required=True, load_only = True)
    department = fields.Nested(PlainDepartmentSchema(), dump_only = True)




    
    
