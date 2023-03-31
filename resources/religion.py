import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ReligionSchema
from models import ReligionModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blueprint = Blueprint("religions", __name__, description="Operations on religions")

@blueprint.route("/religion/<string:religion_id>")
class Religion(MethodView):
    @blueprint.response(200, ReligionSchema)
    def get(self, religion_id):
        religion = ReligionModel.query.get_or_404(religion_id)
        return religion
    
    def delete(self, religion_id):
        religion = ReligionModel.query.get_or_404(religion_id)
        db.session.delete(religion)
        db.session.commit()
        
        return {"message": "Item deleted!"}
            
@blueprint.route("/religion")
class ReligionList(MethodView):
    @blueprint.response(200, ReligionSchema(many=True))
    def get(self):
        return ReligionModel.query.all()
    
    @blueprint.arguments(ReligionSchema)
    @blueprint.response(201, ReligionSchema)
    def post(self, religion_data):
        religion = ReligionModel(**religion_data)
        
        try:
            db.session.add(religion)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "An error occured!")
        except SQLAlchemyError:
            abort(500, message = "An error occured!")
        
        return religion
