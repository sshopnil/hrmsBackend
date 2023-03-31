from db import db

class EmployeeModel(db.Model):
    __tablename__ = "employees"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable= False)
    user_name = db.Column(db.String(80), unique = True, nullable= False)
    phone = db.Column(db.String(80), unique = False, nullable= False)
    dob = db.Column(db.String(10), unique = False, nullable= False)
    address_perm = db.Column(db.String(80), unique = False, nullable= False)
    address_curr = db.Column(db.String(80), unique = False, nullable= False)
    
    religion_id = db.Column(db.Integer, db.ForeignKey("religions.id"), unique = False, nullable = False)
    religion = db.relationship("ReligionModel", back_populates = "employees")
    
    marital_status_id = db.Column(db.Integer, db.ForeignKey("marital_statuses.id"), unique = False, nullable = False)
    marital_status = db.relationship("MaritalStatusModel", back_populates = "employees")
    
    #office_post = db.relationship("OfficePostModel", back_populates = "employee", lazy = "dynamic")
    
    
    