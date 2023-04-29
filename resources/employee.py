import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import EmployeeSchema, EmployeeUpdateSchema
from models import EmployeeModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import hashlib
from schemas import LoginRequestSchema, LoginResponseSchema
from schemas import ChangePasswordRequestSchema, ChangePasswordResponseSchema

blueprint = Blueprint("employees", __name__, description="Operations on employees")

@blueprint.route("/employee/<string:employee_id>")
class Employee(MethodView):
    @blueprint.response(200, EmployeeSchema)
    def get(self, employee_id):
        employee = EmployeeModel.query.get_or_404(employee_id)
        return employee
    
    @blueprint.arguments(EmployeeUpdateSchema)
    @blueprint.response(200, EmployeeSchema)
    def put(self, employee_data, employee_id):
        employee = EmployeeModel.query.get(employee_id)
        
        if employee:
            employee.name = employee_data["name"]
            employee.user_name = employee_data["user_name"]
            employee.phone = employee_data["phone"]
            employee.dob = employee_data["dob"]
            employee.address_perm = employee_data["address_perm"]
            employee.address_curr = employee_data["address_curr"]
            employee.religion_id = employee_data["religion_id"]
            employee.marital_status_id = employee_data["marital_status_id"]
            employee.user_image = employee_data["user_image"]
        else:
            employee = EmployeeModel(employee_id, **employee_data)
            
        db.session.add(employee)
        db.session.commit()
        
        return employee
    
    def delete(self, employee_id):
        employee = EmployeeModel.query.get_or_404(employee_id)
        db.session.delete(employee)
        db.session.commit()
        
        return {"message": "Employee deleted!"}
            
@blueprint.route("/employee")
class EmployeeList(MethodView):
    @blueprint.response(200, EmployeeSchema(many=True))
    def get(self):
        return EmployeeModel.query.all()
    
    @blueprint.arguments(EmployeeSchema)
    @blueprint.response(201, EmployeeSchema)
    def post(self, employee_data):
        employee = EmployeeModel(**employee_data)
        generic_password = "12345"
        generic_password_hashed = hashlib.sha256(generic_password.encode()).hexdigest()
        employee.password = generic_password_hashed
        
        try:
            db.session.add(employee)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "An error occured!")
        except SQLAlchemyError as e:
            abort(500, message = str(employee_data))
        
        return employee
    
@blueprint.route("/employee/user_name/<string:user_name>")
class EmployeeList(MethodView):
    @blueprint.response(200, EmployeeSchema)
    def get(self, user_name):
        employee = EmployeeModel.query.filter_by(user_name=user_name).first()
        return employee

    
@blueprint.route("/employee/login")
class Login(MethodView):
    @blueprint.arguments(LoginRequestSchema)
    @blueprint.response(200, LoginResponseSchema)
    def post(self, login_data):
        user_name = login_data["user_name"]
        password_input = login_data["password"]
        password_input_hashed = hashlib.sha256(password_input.encode()).hexdigest()
        
        employee = EmployeeModel.query.filter_by(user_name=user_name).first()
        
        if employee.password == password_input_hashed:
            if employee.password == "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5":
                return {"login_status": "success", "change_password_status": 0}
            else:
                return {"login_status": "success", "change_password_status": 1}
        else:
            return {"login_status": "failure", "change_password_status": 0}
    
@blueprint.route("/employee/change_password")
class Login(MethodView):
    @blueprint.arguments(ChangePasswordRequestSchema)
    @blueprint.response(200, ChangePasswordResponseSchema)
    def post(self, change_password_data):
        user_name = change_password_data["user_name"]
        password_changed = change_password_data["password"]
        
        employee = EmployeeModel.query.filter_by(user_name=user_name).first()
        password_changed_hashed = hashlib.sha256(password_changed.encode()).hexdigest()
        employee.password = password_changed_hashed
        
        db.session.add(employee)
        db.session.commit()
        
        return {"change_password_status": 1}
        
        
        
        
