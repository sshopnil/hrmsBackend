from db import db

class DepartmentModel(db.Model):
    __tablename__ = "departments"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable= False)
    office_posts = db.relationship("OfficePostModel", back_populates = "department", lazy = "dynamic")
    