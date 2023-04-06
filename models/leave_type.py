from db import db

class LeaveTypeModel(db.Model):
    __tablename__ = "leave_types"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable= False)
    leaves = db.relationship("LeaveModel", back_populates = "leave_type", lazy = "dynamic")