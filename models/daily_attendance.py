from db import db

class DailyAttendanceModel(db.Model):
    __tablename__ = "daily_attendances"
    
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(10), unique = False, nullable= False)
    
    day = db.Column(db.Integer, unique = False, nullable = True)
    month = db.Column(db.Integer, unique = False, nullable = True)
    year = db.Column(db.Integer, unique = False, nullable = True)
    
    
    office_entry_time = db.Column(db.String(10), unique = False, nullable= False)
    office_exit_time = db.Column(db.String(10), unique = False, nullable= False)
    
    late_status = db.Column(db.Integer, unique = False)
    late_cause = db.Column(db.String(100), unique = False)
    
    late_approval_status = db.Column(db.Integer, unique = False, default = 0)
    
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), unique = False)
    employee = db.relationship("EmployeeModel", back_populates = "daily_attendances")
    
