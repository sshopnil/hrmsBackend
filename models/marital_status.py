from db import db

class MaritalStatusModel(db.Model):
    __tablename__ = "marital_statuses"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable= False)
    employees = db.relationship("EmployeeModel", back_populates = "marital_status", lazy = "dynamic")