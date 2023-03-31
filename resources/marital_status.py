import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import MaritalStatusSchema
from models import MaritalStatusModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blueprint = Blueprint("marital_status", __name__, description="Operations on marital status")

@blueprint.route("/marital_status/<string:marital_status_id>")
class MaritalStatus(MethodView):
    @blueprint.response(200, MaritalStatusSchema)
    def get(self, marital_status_id):
        marital_status = MaritalStatusModel.query.get_or_404(marital_status_id)
        return marital_status
    
    def delete(self, marital_status_id):
        marital_status = MaritalStatusModel.query.get_or_404(marital_status_id)
        db.session.delete(marital_status)
        db.session.commit()
        
        return {"message": "MS deleted!"}
            
@blueprint.route("/marital_status")
class MaritalStatusList(MethodView):
    @blueprint.response(200, MaritalStatusSchema(many=True))
    def get(self):
        return MaritalStatusModel.query.all()
    
    @blueprint.arguments(MaritalStatusSchema)
    @blueprint.response(201, MaritalStatusSchema)
    def post(self, marital_status_data):
        marital_status = MaritalStatusModel(**marital_status_data)
        
        try:
            db.session.add(marital_status)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "An error occured!")
        except SQLAlchemyError:
            abort(500, message = "An error occured!")
        
        return marital_status
