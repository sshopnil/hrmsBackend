import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import OfficePostSchema
from models import OfficePostModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blueprint = Blueprint("office_posts", __name__, description="Operations on office_posts")

@blueprint.route("/office_post/<string:office_post_id>")
class OfficePost(MethodView):
    @blueprint.response(200, OfficePostSchema)
    def get(self, office_post_id):
        office_post = OfficePostModel.query.get_or_404(office_post_id)
        return office_post
    
    """
    @blueprint.arguments(OfficePostUpdateSchema)
    @blueprint.response(200, OfficePostSchema)
    def put(self, office_post_id, employee_id):
        
        office_post = OfficePostModel.query.get(office_post_id)
    
        office_post[employee_id] = employee_id
        
            
        db.session.add(office_post)
        db.session.commit()
        
        return office_post
    """          
@blueprint.route("/office_post")
class OfficePostList(MethodView):
    @blueprint.response(200, OfficePostSchema(many=True))
    def get(self):
        return OfficePostModel.query.all()
    
    @blueprint.arguments(OfficePostSchema)
    @blueprint.response(201, OfficePostSchema)
    def post(self, office_post_data):
        office_post = OfficePostModel(**office_post_data)
        
        try:
            db.session.add(office_post)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "An error occured!")
        except SQLAlchemyError as e:
            abort(500, message = str(e))
        
        return office_post
