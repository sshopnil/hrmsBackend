import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import EmployeeSchema, EmployeeUpdateSchema
from models import EmployeeModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

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
        
        try:
            db.session.add(employee)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "An error occured!")
        except SQLAlchemyError as e:
            abort(500, message = str(employee_data))
        
        return employee
