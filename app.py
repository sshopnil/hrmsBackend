from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate

from db import db
import models
import os

from resources.religion import blueprint as ReligionBlueprint
from resources.marital_status import blueprint as MaritalStatusBlueprint
from resources.employee import blueprint as EmployeeBlueprint
from resources.office_post import blueprint as OfficePostBlueprint
from resources.department import blueprint as DepartmentBlueprint
from resources.office import blueprint as OfficeBlueprint
from resources.leave_type import blueprint as LeaveTypeBlueprint
from resources.leave import blueprint as LeaveBlueprint
from resources.daily_attendance import blueprint as DailyAttendanceBlueprint

from flask_cors import CORS

def create_app():

    app = Flask(__name__, instance_path=os.getcwd())
    CORS(app)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "HRMS REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    #app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch = True)
    

    api = Api(app)

    api.register_blueprint(ReligionBlueprint)
    api.register_blueprint(MaritalStatusBlueprint)
    api.register_blueprint(EmployeeBlueprint)
    
    api.register_blueprint(OfficePostBlueprint)
    api.register_blueprint(DepartmentBlueprint)
    api.register_blueprint(OfficeBlueprint)
    
    api.register_blueprint(LeaveBlueprint)
    api.register_blueprint(LeaveTypeBlueprint)
    
    api.register_blueprint(DailyAttendanceBlueprint)
    
    
    
    return app


