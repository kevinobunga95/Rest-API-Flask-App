from flask import jsonify
from flask_smorest import Blueprint, abort
from models import UserModel
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from db import db
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from schema import UserLoginSchema, UserRegisterSchema, UpdateUserRegisterSchema, UpdatePasswordSchema
from blocklist import BLOCKLIST

blp = Blueprint("Users", "users", description="users log in details")


@blp.route("/sign-up")
class UserRegister(MethodView):

    @blp.arguments(UserRegisterSchema)
    @blp.response(200, UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="The username already exists")

        user = UserModel(first_name=user_data["first_name"],
                         last_name=user_data["last_name"],
                         email=user_data["email"],
                         username=user_data["username"],
                         password=pbkdf2_sha256.hash(user_data["password"]))

        db.session.add(user)
        db.session.commit()

        return jsonify({"Message": "Registration successful"})

    @blp.response(200, UserRegisterSchema(many=True))
    def get(self):
        all_user = UserModel.query.all()

        return all_user


@blp.route("/sign-up/<int:id>")
class UserManagement(MethodView):
    @blp.response(200, UserRegisterSchema)
    def get(self, id):
        user = UserModel.query.get_or_404(id)
        return user

    @blp.arguments(UpdateUserRegisterSchema)
    @blp.response(200, UpdateUserRegisterSchema)
    def put(self, user_data, id):

        user = UserModel.query.get_or_404(id)

        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.email = user_data["email"]
        user.username = user_data["username"]

        db.session.add(user)

        db.session.commit()

        return user

    @jwt_required()
    def delete(self, id):

        jwt = get_jwt()
        if not jwt.get("is admin"):
            abort(401, message="Admin privilege required")
        try:
            user = UserModel.query.get_or_404(id)

            db.session.delete(user)
            db.session.commit()

            return jsonify({"message": "The user details deleted successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    @blp.response(201, UserLoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        try:
            if user and pbkdf2_sha256.verify(user_data["password"], user.password):
                access_token = create_access_token(identity=user.id)

                return jsonify({"access_toke": access_token})

            abort(401, message="Incorrect username or password")

        except ValueError:

            return jsonify({"Message": "Incorrect password"})


@blp.route("/forget-password/<int:id>")
class ChangePassword(MethodView):

    @blp.arguments(UpdatePasswordSchema)
    def put(self, user_data, id):
        user = UserModel.query.get(id)

        if user.username == user_data["username"]:
            user.username = user_data["username"]
            user.password = pbkdf2_sha256.hash(user_data["password"])
        else:
            abort(400, message="user does not exist")
        db.session.add(user)

        db.session.commit()

        return jsonify({"message": "Password successfully changed"})


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jwt = get_jwt()
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)

        return {"message": "Successfully logged out"}
