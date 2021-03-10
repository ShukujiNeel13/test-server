import time
import json
from pprint import pprint
from flask import Flask, request, make_response, jsonify
import jwt

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Echoes back the request body as response body if one is given."""

    request_status = f'{request.method} request received on index.'
    print(request_status)
    response_data = {'status': request_status}

    request_body = request.data

    if request_body:
        print('Request body given is:')
        pprint(request_body)
        # request_body_json_string = request_body.decode('utf-8')
        # request_body_dict = json.loads(request_body_json_string)
        # response_data['data'] = request_body_dict
        # print('Request body given is:')
        # pprint(request_body_dict)

    request_headers = request.headers

    if request_headers:
        print('Request Headers given as:')
        pprint(request_headers)

    # return {'name': 'neel'}
    # make_response()
    # return make_response('success')

    return make_response(jsonify(response_data), 200)


@app.route('/index_with_delay', methods=['GET', 'POST'])
def index_with_delay():

    print('Request received on /index_with_delay')
    time.sleep(9)
    return make_response(jsonify({'status': 'success'}), 200)


@app.route('/login', methods=['GET', 'POST'])
def auth_login():
    """Returns a dummy token in response body"""

    request_status = f'{request.method} request received on /login'
    print(request_status)

    # response_data = {'status': request_status, 'token': 'dummy_token'}

    request_body = request.data
    if request_body:
        request_body_json_string = request_body.decode('utf-8')
        request_body_dict = json.loads(request_body_json_string)
        # response_data['data'] = request_body_dict
        print('Request body given is:')
        pprint(request_body_dict)

    # TODO: Create a JWT which has exp that will expire in desired duration from current time.
    seconds_to_expire_token = 12
    current_unix_time = int(time.time())
    unix_time_to_expire_token = current_unix_time + seconds_to_expire_token

    token_data = {
        'exp': unix_time_to_expire_token
    }

    encoded_token = jwt.encode(token_data, 'random')

    # response_data = {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI3NjZjYmI3Ni02Njk4LTQ1NWYtOTI2NS0wYmMxNTJhNDFmMDUiLCJleHAiOjE2MTQ3Mzg5MTR9.q5mnw0M7dRko2eU6wyPkdiZR3o7R5AjIwn4qTygMWmw'}

    response_data = {'token': encoded_token}

    return make_response(jsonify(response_data), 200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
