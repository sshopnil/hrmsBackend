import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import DepartmentSchema
from models import DepartmentModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blueprint = Blueprint("departments", __name__, description="Operations on departments")

@blueprint.route("/department/<string:department_id>")
class Department(MethodView):
    @blueprint.response(200, DepartmentSchema)
    def get(self, department_id):
        department = DepartmentModel.query.get_or_404(department_id)
        return department
            
@blueprint.route("/department")
class DepartmentList(MethodView):
    @blueprint.response(200, DepartmentSchema(many=True))
    def get(self):
        return DepartmentModel.query.all()
    
    @blueprint.arguments(DepartmentSchema)
    @blueprint.response(201, DepartmentSchema)
    def post(self, department_data):
        department = DepartmentModel(**department_data)
        
        try:
            db.session.add(department)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "An error occured!")
        except SQLAlchemyError:
            abort(500, message = "An error occured!")
        
        return department
