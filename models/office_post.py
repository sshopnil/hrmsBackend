from db import db

class OfficePostModel(db.Model):
    __tablename__ = "office_posts"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable= False)
    parent_id = db.Column(db.Integer, nullable = False)
    
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), unique = False, nullable = False)
    department = db.relationship("DepartmentModel", back_populates = "office_posts")
    
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), unique = False, nullable = True)
    employee = db.relationship("EmployeeModel", back_populates = "_office_post")
    
    
    
    
    