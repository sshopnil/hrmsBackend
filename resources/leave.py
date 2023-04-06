import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import LeaveSchema, LeaveTypeSchema, LeaveUpdateSchema
from models import LeaveModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import hashlib

blueprint = Blueprint("leaves", __name__, description="Operations on leaves")

@blueprint.route("/leave/<string:leave_id>")
class Leave(MethodView):
    @blueprint.response(200, LeaveSchema)
    def get(self, leave_id):
        leave = LeaveModel.query.get_or_404(leave_id)
        return leave
    
    @blueprint.arguments(LeaveUpdateSchema)
    @blueprint.response(200, LeaveSchema)
    def put(self, leave_data, leave_id):
        leave = LeaveModel.query.get(leave_id)
        
        leave.leave_approval_status = leave_data["leave_approval_status"]
        db.session.add(leave)
        db.session.commit()
        
        return leave
    
    
            
@blueprint.route("/leave")
class LeaveList(MethodView):
    @blueprint.response(200, LeaveSchema(many=True))
    def get(self):
        return LeaveModel.query.all()
    
    @blueprint.arguments(LeaveSchema)
    @blueprint.response(201, LeaveSchema)
    def post(self, leave_data):
        leave = LeaveModel(**leave_data)
        leave.leave_approval_status = 0
        
        try:
            db.session.add(leave)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "An error occured!")
        except SQLAlchemyError as e:
            abort(500, message = str(leave_data))
        
        return leave
    
@blueprint.route("/leave/leave_approval_status/<string:leave_approval_status>")
class LeaveListOnApproval(MethodView):
    @blueprint.response(200, LeaveSchema(many=True))
    def get(self, leave_approval_status):
        return LeaveModel.query.filter_by(leave_approval_status = leave_approval_status)
        
    
    