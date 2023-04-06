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
    #password = fields.Str(required=True)
    
class PlainLeaveTypeSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    
class PlainLeaveSchema(Schema):
    id = fields.Integer(dump_only=True)
    leave_start_date = fields.Str(required=True)
    leave_end_date = fields.Str(required=True)
    leave_approval_status = fields.Integer(required=True)
    
class LeaveTypeSchema(PlainLeaveTypeSchema):
    leaves = fields.List(fields.Nested(PlainLeaveSchema, dump_only = True))
    
class LeaveSchema(PlainLeaveSchema):
    leave_type_id = fields.Int(required=True, load_only = True)
    leave_type = fields.Nested(PlainLeaveTypeSchema(), dump_only = True)
    
    employee_id = fields.Int(required=True, load_only = True)
    employee = fields.Nested(PlainEmployeeSchema(), dump_only = True)

class EmployeeUpdateSchema(Schema):
    name = fields.Str()
    user_name = fields.Str()
    phone = fields.Str()
    dob = fields.Str()
    address_perm = fields.Str()
    address_curr = fields.Str()
    
    religion_id = fields.Int()
    marital_status_id = fields.Int()
    password = fields.Str()
    
class ReligionSchema(PlainReligionSchema):
    employees = fields.List(fields.Nested(PlainEmployeeSchema), dump_only = True)

class MaritalStatusSchema(PlainMaritalStatusSchema):
    employees = fields.List(fields.Nested(PlainEmployeeSchema), dump_only = True)

class EmployeeSchema(PlainEmployeeSchema):
    religion_id = fields.Int(required=True, load_only = True)
    religion = fields.Nested(PlainReligionSchema(), dump_only = True)
    
    marital_status_id = fields.Int(required=True, load_only = True)
    marital_status = fields.Nested(PlainMaritalStatusSchema(), dump_only = True)
    
    _office_post = fields.Nested(PlainEmployeeSchema(), dump_only = True)
    
    leaves = fields.List(fields.Nested(PlainLeaveSchema(), dump_only = True))

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
    
    employee_id = fields.Int(load_only = True)
    employee = fields.Nested(PlainEmployeeSchema(), dump_only = True)
    

class OfficeSchema(Schema):
    id = fields.Integer(dump_only=True)
    phone = fields.Str(required=True)
    email = fields.Str(required=True)
    address = fields.Str(required=True)
    website = fields.Str(required=True)
    
class OfficeUpdateSchema(Schema):
    phone = fields.Str()
    email = fields.Str()
    address = fields.Str()
    website = fields.Str()
    
class OfficePostUpdateSchema(Schema):
    name = fields.Str()
    parent_id = fields.Integer()
    department_id = fields.Integer()
    employee_id = fields.Integer()
    
class LoginRequestSchema(Schema):
    user_name = fields.Str()
    password = fields.Str()
    
class LoginResponseSchema(Schema):
    login_status = fields.Str()
    change_password_status = fields.Integer()

class ChangePasswordRequestSchema(Schema):
    user_name = fields.Str()
    password = fields.Str()
    
class ChangePasswordResponseSchema(Schema):
    change_password_status = fields.Integer()

class LeaveUpdateSchema(Schema):
    leave_type_id = fields.Integer()
    leave_start_date = fields.Str()
    leave_end_date = fields.Str()
    leave_approval_status = fields.Integer()
    employee_id = fields.Integer()
    
    
    


    
    

    
    
