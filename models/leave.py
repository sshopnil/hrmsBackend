from db import db

class LeaveModel(db.Model):
    __tablename__ = "leaves"
    
    id = db.Column(db.Integer, primary_key = True)
    
    leave_type_id = db.Column(db.Integer, db.ForeignKey("leave_types.id"), unique = False, nullable = False)
    leave_type = db.relationship("LeaveTypeModel", back_populates = "leaves")
    
    leave_start_date = db.Column(db.String(10), unique = False, nullable= False)
    leave_end_date = db.Column(db.String(10), unique = False, nullable= False)
    
    leave_approval_status = db.Column(db.Integer, unique = False, nullable = False)
    
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), unique = False, nullable = True)
    employee = db.relationship("EmployeeModel", back_populates = "leaves")
    
    
    
    
    
    
