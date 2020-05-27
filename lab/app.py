from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
from flask import jsonify
from flask import redirect
from flask import url_for
from crypto import EDDSASigner
from config_lab import LAB
import datetime
import os
import requests

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from models import *


@app.route('/doctor')
def doctor_panel():
    status = request.args.get('status')
    regions = AvailableRegion.query.all()
    test_systems = TestSystem.query.all()

    doctor = Doctor.query.get(1)
    return render_template('doctor.html', status=status, regions=regions, test_systems=test_systems,
                           platform_url=LAB['PLATFORM_URL'], lab_name=doctor.laboratory.lab_name, doctor=doctor)


@app.route('/superadmin')
@app.route('/superadmin/admins')
def superadmin_panel_admins():
    admins = Admin().query.all()

    superadmin = SuperAdmin.query.get(1)
    return render_template('/superadmin/admins.html', superadmin=superadmin, data=admins)


@app.route('/superadmin/doctors')
def superadmin_panel_doctors():
    data = []

    doctors = Doctor().query.all()
    for row in doctors:
        data_item = dict()
        data_item['id'] = row.id
        data_item['first_name'] = row.first_name
        data_item['last_name'] = row.last_name
        data_item['patronymic'] = row.patronymic
        data_item['username'] = row.username
        data_item['laboratory'] = row.laboratory.lab_name
        data_item['address'] = row.laboratory.address

        data.append(data_item)

    superadmin = SuperAdmin.query.get(1)
    return render_template('/superadmin/doctors.html', superadmin=superadmin, data=data)


@app.route('/superadmin/passes')
def superadmin_panel_passes():
    data = []

    passes = Pass().query.all()
    for row in passes:
        data_item = dict()
        data_item['analysis_id'] = row.analysis_id
        data_item['sid'] = row.sid
        data_item['first_name'] = row.first_name
        data_item['last_name'] = row.last_name
        data_item['patronymic'] = row.patronymic
        data_item['birthday'] = row.birthday.strftime('%d.%m.%Y')
        data_item['passport'] = str(row.passport_series) + ' ' + str(row.passport_number)
        data_item['doctor'] = row.doctor.first_name + ' ' + row.doctor.last_name + ' ' + row.doctor.patronymic
        data_item['laboratory'] = row.doctor.laboratory.lab_name
        data_item['region'] = row.available_region.region_name

        data.append(data_item)

    superadmin = SuperAdmin.query.get(1)
    return render_template('/superadmin/passes.html', superadmin=superadmin, data=data)


@app.route('/admin')
@app.route('/admin/doctors')
def admin_panel_doctors():
    data = []

    doctors = Doctor().query.all()
    for row in doctors:
        data_item = dict()
        data_item['id'] = row.id
        data_item['first_name'] = row.first_name
        data_item['last_name'] = row.last_name
        data_item['patronymic'] = row.patronymic
        data_item['username'] = row.username
        data_item['laboratory'] = row.laboratory.lab_name
        data_item['address'] = row.laboratory.address

        data.append(data_item)

    admin = Admin.query.get(1)
    return render_template('/admin/doctors.html', admin=admin, data=data)


@app.route('/admin/passes')
def admin_panel_passes():
    data = []

    passes = Pass().query.all()
    for row in passes:
        data_item = dict()
        data_item['analysis_id'] = row.analysis_id
        data_item['sid'] = row.sid
        data_item['first_name'] = row.first_name
        data_item['last_name'] = row.last_name
        data_item['patronymic'] = row.patronymic
        data_item['birthday'] = row.birthday.strftime('%d.%m.%Y')
        data_item['passport'] = str(row.passport_series) + ' ' + str(row.passport_number)
        data_item['doctor'] = row.doctor.first_name + ' ' + row.doctor.last_name + ' ' + row.doctor.patronymic
        data_item['laboratory'] = row.doctor.laboratory.lab_name
        data_item['region'] = row.available_region.region_name

        data.append(data_item)

    admin = Admin.query.get(1)
    return render_template('/admin/passes.html', admin=admin, data=data)


@app.route('/get_qr_data', methods=['POST'])
def get_qr_data():
    data = request.get_json()
    signer = EDDSASigner(f'{data["lastname"]} {data["firstname"]} {data["patronymic"]} {data["birthday"]} '
                         f'{data["salt"]}')
    signature = signer.get_signed_data().decode('utf8')
    data['sid'] = signature
    data['lab_id'] = LAB['ID']
    return jsonify(data)


@app.route('/save_pass_data', methods=['POST'])
def save_pass_data():
    form_data = request.form.copy()
    pass_data = Pass(analysis_id=form_data['analysis_id'], sid=form_data['sid'], salt=form_data['salt'],
                     first_name=form_data['firstname'], last_name=form_data['lastname'],
                     patronymic=form_data['patronymic'],
                     birthday=datetime.strptime(form_data['date_birthday'], '%d.%m.%Y'),
                     passport_series=form_data['passport_series'], passport_number=form_data['passport_number'],
                     pass_status=True, receive_analysis_date=datetime.strptime(form_data['date_analysis'], '%d.%m.%Y'),
                     pass_expiration_date=datetime.strptime(form_data['date_end'], '%d.%m.%Y'),
                     test_system_id=form_data['test_system'], doctor_id=1,
                     available_region_id=form_data['available_region'])
    db.session.add(pass_data)
    db.session.commit()

    platform_data = dict()
    platform_data['sid'] = form_data['sid']
    platform_data['salt'] = form_data['salt']
    platform_data['receive_analysis_date'] = form_data['date_analysis']
    platform_data['pass_expiration_date'] = form_data['date_end']
    platform_data['pass_status'] = True
    platform_data['test_system_name'] = TestSystem.query.get(form_data['test_system']).name
    platform_data['manufacturer'] = TestSystem.query.get(form_data['test_system']).manufacturer
    platform_data['certificate'] = TestSystem.query.get(form_data['test_system']).certificate
    platform_data['available_region'] = AvailableRegion.query.get(form_data['available_region']).region_name
    platform_data['lab_id'] = LAB['ID']

    signer = EDDSASigner(f"{platform_data['sid']} {platform_data['salt']} {platform_data['receive_analysis_date']} "
                         f"{platform_data['pass_expiration_date']} {platform_data['pass_status']} "
                         f"{platform_data['test_system_name']} {platform_data['manufacturer']} "
                         f"{platform_data['certificate']} {platform_data['available_region']} "
                         f"{platform_data['lab_id']}")

    platform_data['signature'] = signer.get_signed_data().decode('utf8')

    resp = requests.post(LAB['PLATFORM_URL'] + '/save_data', json=platform_data)
    print(resp.text)

    return redirect(url_for('doctor_panel', status='success'))
