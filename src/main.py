import os

from flask import Flask

from init import db, ma, bcrypt, jwt
from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400
    
    
    @app.errorhandler(400)
    def bad_request(err):
        return {"error": err.messages}, 400

    @app.errorhandler(401)
    def unauthenticated():
        return {"error": "You are not authenticated"}, 401

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.group_controller import groups_bp
    app.register_blueprint(groups_bp)


    return app