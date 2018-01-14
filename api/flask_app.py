import os
import re
from functools import wraps

import yaml
from flask import Flask, jsonify, request, make_response

from api.authentication import Authentication
from dao_factory import DAO_Factory

app = Flask(__name__)


def authenticate(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        auth = Authentication(request)
        if not auth.authenticate():
            return jsonify(auth.error)
        return func(*args, **kwargs)
    return new_func


@app.route('/get_responses')
@authenticate
def get_all_responses():
    responses = dao.get_all_responses()
    resp = jsonify(responses)
    return resp


@app.route('/get_responses/<service>')
@authenticate
def get_service_responses(service):
    valid = re.match('[ąężźćńłóśa-zA-Z0-9\-.]+\.\w+', service)
    if not valid:
        return jsonify({'bad domain name:': service})
    responses = dao.get_service_responses(service)
    resp = jsonify(responses)
    return resp


@app.route('/get_code_responses/<code>')
@authenticate
def get_code_responses(code):
    code = ''.join(re.findall('\d+', code))
    responses = dao.get_code_responses(code)
    return jsonify(responses)


@app.errorhandler(404)
def not_found(*args):
    response = ['404', 'not found']
    return make_response(jsonify(response), 404)


if __name__ == "__main__":
    app_config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "app_config.yml")
    with open(app_config_path) as file:
        app_config = yaml.load(file)
    dao = DAO_Factory().get_dao(app_config['database'])
    app.run()
