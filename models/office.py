from db import db

class OfficeModel(db.Model):
    __tablename__ = "offices"
    
    id = db.Column(db.Integer, primary_key = True)
    phone = db.Column(db.String(80), unique = True, nullable= False)
    email = db.Column(db.String(80), unique = True, nullable= False)
    address = db.Column(db.String(500), unique = False, nullable= False)
    website = db.Column(db.String(10), unique = True, nullable= False)