from app import db
from datetime import datetime


class SuperAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    patronymic = db.Column(db.String(64), index=True)
    privileged_admins = db.relationship('Admin', backref='privileged_by', lazy='dynamic')

    def __repr__(self):
        return '<SuperAdmin {}>'.format(self.username)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    patronymic = db.Column(db.String(64), index=True)
    privileged_by_id = db.Column(db.Integer, db.ForeignKey('super_admin.id'))
    privileged_doctors = db.relationship('Doctor', backref='privileged_by', lazy='dynamic')

    def __repr__(self):
        return '<Admin {}>'.format(self.username)


class TestSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    manufacturer = db.Column(db.String(64))
    certificate = db.Column(db.String(64))
    passes = db.relationship('Pass', backref='test_system', lazy='dynamic')

    def __repr__(self):
        return '<TestSystem {}>'.format(self.name)


class Pass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.String(64), index=True)
    sid = db.Column(db.String(128), unique=True)
    salt = db.Column(db.String(20))
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    patronymic = db.Column(db.String(64), index=True)
    birthday = db.Column(db.DateTime, index=True)
    passport_series = db.Column(db.Integer, index=True)
    passport_number = db.Column(db.Integer, index=True)
    pass_status = db.Column(db.Boolean, index=True)
    receive_analysis_date = db.Column(db.DateTime, index=True)
    pass_expiration_date = db.Column(db.DateTime, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    test_system_id = db.Column(db.Integer, db.ForeignKey('test_system.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    available_region_id = db.Column(db.Integer, db.ForeignKey('available_region.id'))

    def __repr__(self):
        return '<Pass #{}>'.format(self.id)


class Laboratory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lab_name = db.Column(db.String(64), index=True)
    address = db.Column(db.String(64), index=True)
    person_first_name = db.Column(db.String(64), index=True)
    person_last_name = db.Column(db.String(64), index=True)
    person_patronymic = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(50))
    doctors = db.relationship('Doctor', backref='laboratory', lazy='dynamic')

    def __repr__(self):
        return '<Laboratory {}>'.format(self.lab_name)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    patronymic = db.Column(db.String(64), index=True)
    laboratory_id = db.Column(db.Integer, db.ForeignKey('laboratory.id'))
    passes = db.relationship('Pass', backref='doctor', lazy='dynamic')
    privileged_by_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return '<Doctor {}>'.format(self.username)


class AvailableRegion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(64), index=True, unique=True)
    passes = db.relationship('Pass', backref='available_region', lazy='dynamic')

    def __repr__(self):
        return '<AvailableRegion {}>'.format(self.region_name)
