import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import LeaveTypeSchema
from models import LeaveTypeModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blueprint = Blueprint("leave_type", __name__, description="Operations on leave type")

@blueprint.route("/leave_type/<string:leave_type_id>")
class LeaveType(MethodView):
    @blueprint.response(200, LeaveTypeSchema)
    def get(self, leave_type_id):
        leave_type = LeaveTypeModel.query.get_or_404(leave_type_id)
        return leave_type
    
            
@blueprint.route("/leave_type")
class LeaveTypeList(MethodView):
    @blueprint.response(200, LeaveTypeSchema(many=True))
    def get(self):
        return LeaveTypeModel.query.all()
    
    @blueprint.arguments(LeaveTypeSchema)
    @blueprint.response(201, LeaveTypeSchema)
    def post(self, leave_type_data):
        leave_type = LeaveTypeModel(**leave_type_data)
        
        try:
            db.session.add(leave_type)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "An error occured!")
        except SQLAlchemyError:
            abort(500, message = "An error occured!")
        
        return leave_type
