import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import LeaveSchema, LeaveTypeSchema, LeaveUpdateSchema, OfficePostSchema, EmployeeSchema, EmployeeLeaveInfoSchema, LeaveApprovalStatus, LeaveTypeStatus
from models import LeaveModel, OfficePostModel
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

"""       
@blueprint.route("/leave/subordinate_leave/<string:office_post_id>")
class LeaveListSubordinate(MethodView):
    @blueprint.response(200, OfficePostSchema(many=True))
    def get_subordinate(self):
        #office_posts_supervisee = OfficePostModel.query.filter_by(parent_id = office_post_id)
        office_posts_supervisee = OfficePostModel.query.all()
        return office_posts_supervisee
"""

@blueprint.route("/leave/subordinate_leave/<string:office_post_id>")
class LeaveList(MethodView):
    @blueprint.response(200, EmployeeLeaveInfoSchema(many=True))
    def get(self, office_post_id):
        office_post_supervisees =  OfficePostModel.query.filter_by(parent_id = office_post_id)
        employee_supervisees = []
        
        for office_post_supervisee in office_post_supervisees:
            employee_supervisee = office_post_supervisee.employee
            employee_supervisees.append(employee_supervisee)
            
        list_employee_leave_info = []
        
        for employee_supervisee in employee_supervisees:
            leaves_employee = LeaveModel.query.filter_by(employee_id = employee_supervisee.id)
            
            for leave_employee in leaves_employee:
                if leave_employee.leave_approval_status == 0: 
                    employee_leave_info = {
                        "leave_id": leave_employee.id,
                        "employee_id": employee_supervisee.id,
                        "employee_name": employee_supervisee.name,
                        "leave_approval_status": leave_employee.leave_approval_status,
                        "leave_start_date": leave_employee.leave_start_date,
                        "leave_end_date": leave_employee.leave_end_date,
                        "leave_type_name": leave_employee.leave_type.name
                    } 
                    print(employee_leave_info)
                
                    list_employee_leave_info.append(employee_leave_info)
        
        unique = { each['leave_id'] : each for each in list_employee_leave_info }.values()
        
        return unique
        
@blueprint.route("/leave/all_statuses")
class LeaveApprovalList(MethodView):
    @blueprint.response(200, LeaveApprovalStatus(many=True))
    def get(self):
        leaves_employee = LeaveModel.query.all()
            
        count_leave_pending = 0
        count_leave_approved = 0
        count_leave_rejected = 0
            
        for leave_employee in leaves_employee:
            if leave_employee.leave_approval_status == 0: 
                count_leave_pending += 1 
            elif leave_employee.leave_approval_status == 1: 
                count_leave_approved += 1
            else:
                count_leave_rejected += 1
        
        leave_pending = {
            "status_id": 0,
            "status_name": "অপেক্ষমান",
            "status_count": count_leave_pending
        }
        
        leave_approved = {
            "status_id": 1,
            "status_name": "অনুমোদিত",
            "status_count": count_leave_approved
        }
        
        leave_rejected = {
            "status_id": 2,
            "status_name": "প্রত্যাখ্যাত",
            "status_count": count_leave_rejected
        }
        
        leave_status_total = []
        
        leave_status_total.append(leave_pending)
        leave_status_total.append(leave_approved)
        leave_status_total.append(leave_rejected)
        
        return leave_status_total
        
@blueprint.route("/leave/all_types")
class LeaveTypeList(MethodView):
    @blueprint.response(200, LeaveTypeStatus(many=True))
    def get(self):
        leaves_employee = LeaveModel.query.all()
            
        count_leave_casual = 0
        count_leave_medical = 0
        count_leave_unpaid = 0
        count_leave_earned = 0
        count_leave_maternity = 0
        
            
        for leave_employee in leaves_employee:
            if leave_employee.leave_type_id == 1: 
                count_leave_casual += 1 
            elif leave_employee.leave_type_id == 2: 
                count_leave_medical += 1
            elif leave_employee.leave_type_id == 3: 
                count_leave_unpaid += 1
            elif leave_employee.leave_type_id == 4: 
                count_leave_earned += 1
            else:
                count_leave_maternity += 1
        
        leave_casual = {
            "type_id": 1,
            "type_name": "ক্যাজুয়াল",
            "type_count": count_leave_casual
        }
        
        leave_medical = {
            "type_id": 2,
            "type_name": "মেডিক্যাল",
            "type_count": count_leave_medical
        }
        
        leave_unpaid = {
            "type_id": 3,
            "type_name": "বিনাবেতন",
            "type_count": count_leave_unpaid
        }
        
        leave_earned = {
            "type_id": 4,
            "type_name": "অর্জিত",
            "type_count": count_leave_earned
        }
        
        leave_maternity = {
            "type_id": 5,
            "type_name": "মাতৃত্বকালীন",
            "type_count": count_leave_maternity
        }
        
        leave_type_total = []
        
        leave_type_total.append(leave_casual)
        leave_type_total.append(leave_medical)
        leave_type_total.append(leave_unpaid)
        leave_type_total.append(leave_earned)
        leave_type_total.append(leave_maternity)
        
        return leave_type_total
  
        

            
  
        
        
        
        
        
        
