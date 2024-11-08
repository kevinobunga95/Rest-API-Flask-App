from db import db


class CompanyModel(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    owner = db.Column(db.String(100), unique=False, nullable=False)


