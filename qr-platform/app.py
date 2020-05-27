from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from crypto import EDDSAVerifier
import json
import os
import base64

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from models import *


@app.route('/check')
def check_code():
    data = request.args.get('data', default=-1)
    if data == -1:
        return render_template('check.html', status='corrupt')
    try:
        data_json = json.loads(base64.b64decode(data).decode('utf8'))
    except:
        return render_template('check.html', status='corrupt')
    valid_keys = {'birthday', 'firstname', 'lab_id', 'lastname', 'patronymic', 'salt', 'sid'}
    for key in data_json:
        if key in valid_keys:
            valid_keys.remove(key)
    if len(valid_keys) > 0:
        return render_template('check.html', status='corrupt')

    plain_text = f'{data_json["lastname"]} {data_json["firstname"]} {data_json["patronymic"]} ' \
                   f'{data_json["birthday"]} {data_json["salt"]}'

    checker = EDDSAVerifier(plain_text, data_json['sid'], LaboratoryCompany.query.get(data_json['lab_id']).edsa_pub_key)
    verified = checker.is_verified()

    if not verified:
        return render_template('check.html', status='corrupt')

    pass_row = Pass.query.filter_by(sid=data_json['sid']).one_or_none()

    if pass_row is not None:
        status = 'valid'
    else:
        status = 'invalid'

    return render_template('check.html', status=status, lastname=data_json['lastname'],
                           firstname=data_json['firstname'], patronymic=data_json['patronymic'],
                           birthday=data_json['birthday'])


@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()
    plain_text = f"{data['sid']} {data['salt']} {data['receive_analysis_date']} {data['pass_expiration_date']} " \
                 f"{data['pass_status']} {data['test_system_name']} {data['manufacturer']} {data['certificate']} " \
                 f"{data['available_region']} {data['lab_id']}"

    data['receive_analysis_date'] = datetime.strptime(data['receive_analysis_date'], '%d.%m.%Y')
    data['pass_expiration_date'] = datetime.strptime(data['pass_expiration_date'], '%d.%m.%Y')

    checker = EDDSAVerifier(plain_text, data['signature'], LaboratoryCompany.query.get(data['lab_id']).edsa_pub_key)
    verified = checker.is_verified()
    if not verified:
        return 'Invalid signature'

    del data['signature']

    pass_data = Pass(**data)
    db.session.add(pass_data)
    db.session.commit()

    return 'Success!'


@app.route('/admin')
@app.route('/admin/labs')
def admin_panel_doctors():
    data = []

    labs = LaboratoryCompany().query.all()
    for row in labs:
        data_item = dict()
        data_item['id'] = row.id
        data_item['company_name'] = row.company_name
        data_item['main_address'] = row.main_address
        data_item['last_name'] = row.director_last_name
        data_item['first_name'] = row.director_first_name
        data_item['patronymic'] = row.director_patronymic
        data_item['phone_number'] = row.phone_number

        data.append(data_item)

    admin = Admin.query.get(1)
    return render_template('/admin/labs.html', admin=admin, data=data)


@app.route('/admin/passes')
def admin_panel_passes():
    data = []

    passes = Pass().query.all()
    for row in passes:
        data_item = dict()
        data_item['id'] = row.id
        data_item['sid'] = row.sid
        data_item['test_system_name'] = row.test_system_name
        data_item['manufacturer'] = row.manufacturer
        data_item['certificate'] = row.certificate
        data_item['available_region'] = row.available_region
        data_item['receive_analysis_date'] = row.receive_analysis_date.strftime('%d.%m.%Y')
        data_item['pass_expiration_date'] = row.pass_expiration_date.strftime('%d.%m.%Y')
        data_item['timestamp'] = row.timestamp.strftime('%d.%m.%Y')

        data.append(data_item)

    admin = Admin.query.get(1)
    return render_template('/admin/passes.html', admin=admin, data=data)


if __name__ == '__main__':
    app.run()
