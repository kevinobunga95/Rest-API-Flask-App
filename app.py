from flask import Flask, jsonify
from flask_smorest import Api
import os
from flask_jwt_extended import JWTManager, get_jwt
from resources.company import blp as CompanyBlueprint
from resources.User import blp as UserBlueprint
from db import db
from blocklist import BLOCKLIST


def create_app():
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "User REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "Kevion"

    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is admin": True}
        return {"is admin": False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def revoked_token_callback(jwt_header, jwt_payback):
        return jsonify({"description": "The token has been revoked"})

    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(CompanyBlueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
