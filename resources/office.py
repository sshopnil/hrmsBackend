import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import OfficeSchema, OfficeUpdateSchema
from models import OfficeModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blueprint = Blueprint("offices", __name__, description="Operations on offices")

@blueprint.route("/office/<string:office_id>")
class Office(MethodView):
    @blueprint.response(200, OfficeSchema)
    def get(self, office_id):
        office = OfficeSchema.query.get_or_404(office_id)
        return office
    
    @blueprint.arguments(OfficeUpdateSchema)
    @blueprint.response(200, OfficeSchema)
    def put(self, office_data, office_id):
        office = OfficeModel.query.get(office_id)
        
        if office:
            office.phone = office_data["phone"]
            office.email = office_data["email"]
            office.address = office_data["address"]
            office.website = office_data["website"]
        else:
            office = OfficeModel( office_id, **office_data)
            
        db.session.add(office)
        db.session.commit()
        
        return office
            
@blueprint.route("/office")
class OfficeList(MethodView):
    @blueprint.response(200, OfficeSchema(many=True))
    def get(self):
        return OfficeModel.query.all()
    
    @blueprint.arguments(OfficeSchema)
    @blueprint.response(201, OfficeSchema)
    def post(self, office_data):
        office = OfficeModel(**office_data)
        
        try:
            db.session.add(office)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "An error occured!")
        except SQLAlchemyError as e:
            abort(500, message = str(office_data))
        
        return office
