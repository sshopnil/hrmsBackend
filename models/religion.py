from db import db

class ReligionModel(db.Model):
    __tablename__ = "religions"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable= False)
    employees = db.relationship("EmployeeModel", back_populates = "religion", lazy = "dynamic")