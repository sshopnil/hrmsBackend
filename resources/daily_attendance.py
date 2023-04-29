import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import DailyAttendanceSchema, DailyAttendanceUpdateSchema, OfficePostSchema, DailyAttendanceStatusSchema
from models import DailyAttendanceModel, OfficePostModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import hashlib

blueprint = Blueprint("daily-attendances", __name__, description="Operations on daily attendances")


@blueprint.route("/daily_attendance_late_apply/<string:daily_attendance_id>")
class DailyAttendanceApply(MethodView):
    
    @blueprint.arguments(DailyAttendanceUpdateSchema)
    @blueprint.response(200, DailyAttendanceSchema)
    def put(self, daily_attendance_data, daily_attendance_id):
        daily_attendance = DailyAttendanceModel.query.get(daily_attendance_id)
        
        daily_attendance.late_approval_status = 1
        daily_attendance.late_cause = daily_attendance_data["late_cause"]
    
        db.session.add(daily_attendance)
        db.session.commit()
        
        return daily_attendance
    
@blueprint.route("/daily_attendance_approve_reject/<string:daily_attendance_id>")
class DailyAttendance(MethodView):
    
    @blueprint.arguments(DailyAttendanceUpdateSchema)
    @blueprint.response(200, DailyAttendanceSchema)
    def put(self, daily_attendance_data, daily_attendance_id):
        daily_attendance = DailyAttendanceModel.query.get(daily_attendance_id)
        
        daily_attendance.late_approval_status = daily_attendance_data["late_approval_status"]
    
        if daily_attendance.late_approval_status == 2:
            daily_attendance.late_status = 0
            
    
        db.session.add(daily_attendance)
        db.session.commit()
        
        return daily_attendance

"""
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
    
"""  
            
@blueprint.route("/daily_attendance")
class DailyAttendanceList(MethodView):
    @blueprint.response(200, DailyAttendanceSchema(many=True))
    def get(self):
        return DailyAttendanceModel.query.all()
    
    @blueprint.arguments(DailyAttendanceSchema)
    @blueprint.response(201, DailyAttendanceSchema)
    def post(self, daily_attendance_data):
        daily_attendance = DailyAttendanceModel(**daily_attendance_data)
        print(daily_attendance.employee_id)
        entry_time = daily_attendance.office_entry_time
        print("entry time:")
        print(entry_time)
        
        if entry_time != None:
            
            hour = entry_time[:2]
            minute = entry_time[3:5]
            
            print('hour:', hour)
            print('minute:', minute)
            
            date = daily_attendance.date
            
            splitted_string = date.split("/")
            
            daily_attendance.month = int(splitted_string[0])
            daily_attendance.day = int(splitted_string[1])
            daily_attendance.year = int(splitted_string[2])
            
            #print(daily_attendance)
            
            if int(hour) < 9:
                daily_attendance.late_status = 0
            elif int(hour) >= 9 and int(minute) == 0:
                daily_attendance.late_status = 0
            else:
                daily_attendance.late_status = 1
                
            
        else:
            daily_attendance.late_status = 2
        
        try:
            db.session.add(daily_attendance)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message = str(e))
        except SQLAlchemyError as e:
            abort(500, message = str(e))
            
        return daily_attendance
    
@blueprint.route("/daily_attendance/<string:date>")
class DailyAttendanceListByDate(MethodView):
    @blueprint.response(200, DailyAttendanceSchema(many=True))
    def get(self, date):
        return DailyAttendanceModel.query.filter_by(date = date)
    
@blueprint.route("/daily_attendance/<string:employee_id>/<string:month>/<string:year>")
class DailyAttendanceList(MethodView):
    @blueprint.response(200, DailyAttendanceSchema(many=True))
    def get(self, employee_id, month, year):
        
        return DailyAttendanceModel.query.filter_by(
            employee_id = employee_id, 
            month = month,
            year = year
        )
        
    
        
"""    
@blueprint.route("/leave/subordinate_leave/<string:office_post_id>")
class LeaveListSubordinate(MethodView):
    @blueprint.response(200, OfficePostSchema(many=True))
    def get_subordinate(self):
        #office_posts_supervisee = OfficePostModel.query.filter_by(parent_id = office_post_id)
        office_posts_supervisee = OfficePostModel.query.all()
        return office_posts_supervisee
"""


@blueprint.route("/daily_attendance/subordinate_late_attendance/<string:office_post_id>")
class LeaveList(MethodView):
    @blueprint.response(200, DailyAttendanceStatusSchema(many=True))
    def get(self, office_post_id):
        office_post_supervisees =  OfficePostModel.query.filter_by(parent_id = office_post_id)
        employee_supervisees = []
        
        for office_post_supervisee in office_post_supervisees:
            employee_supervisee = office_post_supervisee.employee
            employee_supervisees.append(employee_supervisee)
            
        list_employee_attendance_info = []
        
        for employee_supervisee in employee_supervisees:
            daily_attendances_employee = DailyAttendanceModel.query.filter_by(employee_id = employee_supervisee.id)
            
            for daily_attendance_employee in daily_attendances_employee:
                if daily_attendance_employee.late_approval_status == 1: 
                    employee_daily_attendance_info = {
                        "daily_attendance_id": daily_attendance_employee.id,
                        "employee_id": employee_supervisee.id,
                        "employee_name": employee_supervisee.name,
                        "date": daily_attendance_employee.date,
                        "office_entry_time": daily_attendance_employee.office_entry_time,
                        "office_exit_time": daily_attendance_employee.office_exit_time
                    } 
                
                    #print(employee_leave_info)
                
                    list_employee_attendance_info.append(employee_daily_attendance_info)
        
        #unique = { each['leave_id'] : each for each in list_employee_leave_info }.values()
        
        #return unique
        return list_employee_attendance_info
        
      
        
        
        

            
  
        
        
        
        
        
        
