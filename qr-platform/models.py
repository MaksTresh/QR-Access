from app import db
from datetime import datetime


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    patronymic = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Admin {}>'.format(self.username)


class LaboratoryCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    edsa_pub_key = db.Column(db.String(64))
    company_name = db.Column(db.String(64), index=True)
    main_address = db.Column(db.String(64), index=True)
    director_first_name = db.Column(db.String(64), index=True)
    director_last_name = db.Column(db.String(64), index=True)
    director_patronymic = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(50))
    passes = db.relationship('Pass', backref='laboratory_company', lazy='dynamic')

    def __repr__(self):
        return '<LaboratoryCompany {}>'.format(self.company_name)


class Pass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    salt = db.Column(db.String(20))
    receive_analysis_date = db.Column(db.DateTime, index=True)
    pass_expiration_date = db.Column(db.DateTime, index=True)
    pass_status = db.Column(db.Boolean, index=True)
    test_system_name = db.Column(db.String(64), index=True)
    manufacturer = db.Column(db.String(64))
    certificate = db.Column(db.String(64))
    available_region = db.Column(db.String(64), index=True)
    pass_type = db.Column(db.String(64), index=True, nullable=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('laboratory_company.id'))

    def __repr__(self):
        return '<Pass #{}>'.format(self.id)
