from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models import CompanyModel
from db import db
from flask_jwt_extended import jwt_required
from schema import CompanySchema, UpdateCompanySchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("company", __name__, description="company details")


@blp.route("/company")
class CompanyList(MethodView):

    @jwt_required()
    @blp.arguments(CompanySchema)
    @blp.response(201, CompanySchema)
    def post(self, company_data):

        company = CompanyModel(**company_data)

        try:
            db.session.add(company)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="The company already exist")

        return company

    @jwt_required()
    @blp.response(200, CompanySchema(many=True))
    def get(self):
        all_companies = CompanyModel.query.all()

        return all_companies


@blp.route("/company/<int:id>")
class CompanyData(MethodView):
    @jwt_required()
    @blp.response(200, CompanySchema)
    def get(self, id):
        company_data = CompanyModel.query.get_or_404(id)

        return company_data

    @jwt_required()
    @blp.arguments(UpdateCompanySchema)
    @blp.response(200, CompanySchema)
    def put(self, company_data, id):

        company = CompanyModel.query.get(id)

        if company:
            company.name = company_data["name"]
            company.email = company_data["email"]
            company.address = company_data["address"]
            company.owner = company_data["owner"]
        else:
            company = CompanyModel(id=id, **company_data)

        db.session.add(company)
        db.session.commit()

        return company

    def delete(self, id):

        company = CompanyModel.query.get_or_404(id)

        db.session.delete(company)
        db.session.commit()

        return {"message": "The company has been successfully deleted"}
