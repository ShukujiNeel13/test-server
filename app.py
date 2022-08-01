import sys
import time
import json
from pprint import pprint, pformat
from flask import Flask, request, make_response, jsonify
import jwt

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Echoes back the request body as response body if one is given."""

    _request_path = request.path
    request_status = f'{request.method} request received on path: {_request_path}'
    print(request_status)
    response_data = {'status': request_status}

    if request.query_string:
        rqs = request.query_string
        print(f'Query string in request is:\n{rqs}')

    r_content_type = request.content_type
    print(f'Content type of request is: {r_content_type}')

    request_headers = request.headers

    if request_headers:
        print('Request Headers given as:')
        pprint(dict(request_headers))
    else:
        print('No headers given in this request (cannot be!)')

    # request_body = request.data
    request_body = request.data

    if request_body:

        print(f'Type of request body received is: {type(request_body)}')

        print('\nRequest data (raw format) is:')
        print(request_body)

        if 'x-sc-compression-enabled' in request_headers:
            sc_compression_enabled = request_headers['x-sc-compression-enabled']
            print(f'\n "x-sc-compression-enabled" found in headers as: {sc_compression_enabled}')

        # if request_body:
        #
        #     if r_content_type == 'application/json':
        #
        #         try:
        #             _request_body_str = request_body.decode('utf-8')
        #         except (UnicodeDecodeError, AttributeError):
        #             print('\nFailed to decode request body (Request body was unexpected type)!', file=sys.stderr)
        #             return
        #         print('Request body (decoded string is:)')
        #         print(_request_body_str)
        #
        #         # request_body_dict = json.loads(_request_body_str)
        #         # print('Request body given is:')
        #         # pprint(request_body_dict)
        # else:
        #     print('Content Type was not application/json, will print whatever body received')
        #     # print(pformat(request_body))
        #     print(request_body)

    # return {'name': 'neel'}
    # make_response()
    # return make_response('success')

    return make_response(jsonify(response_data), 200)


@app.route('/matrixevents/scparams/v2/actions', methods=['POST'])
def scparams_v2_actions():
    """Echoes back the request body as response body if one is given."""

    _request_path = request.path
    request_status = f'{request.method} request received on path: {_request_path}'
    print(request_status)
    response_data = {'message': request_status}

    r_content_type = request.content_type
    print(f'Content type of request is: {r_content_type}')
    print(f'Type of Content Type in request is: {type(r_content_type)}')

    # request_body = request.data
    request_body = request.data

    if request_body:

        print(f'Type of request body received is: {type(request_body)}')

        if request_body:

            if r_content_type == 'application/json':

                try:
                    _request_body_str = request_body.decode('utf-8')
                except (UnicodeDecodeError, AttributeError):
                    print('\nFailed to decode request body (Request body was unexpected type)!', file=sys.stderr)
                    return
                # print('Request body (decoded string is:)')
                # print(_request_body_str)

                request_body_dict = json.loads(_request_body_str)
                print('Request body given is:')
                pprint(request_body_dict)
        else:
            print('Content Type was not application/json, will print whatever body received')
            # print(pformat(request_body))
            print(request_body)

    request_headers = request.headers

    if request_headers:
        print('Request Headers given as:')
        pprint(request_headers)

    # return {'name': 'neel'}
    # make_response()
    # return make_response('success')
    response_data['code'] = 'SUCCESS'
    return make_response(jsonify(response_data), 200)


@app.route('/index_with_delay', methods=['GET', 'POST'])
def index_with_delay():

    print('Request received on /index_with_delay')
    time.sleep(9)
    return make_response(jsonify({'status': 'success'}), 200)


@app.route('/ping', methods=['GET', 'POST'])
def ping():
    """Echoes back the request body as response body if one is given."""

    _request_path = request.path
    request_status = f'{request.method} request received on path: {_request_path}'
    print(request_status)
    response_data = {'status': request_status}

    r_content_type = request.content_type
    print(f'Content type of request is: {r_content_type}')
    print(f'Type of Content Type in request is: {type(r_content_type)}')

    # request_body = request.data
    request_body = request.data

    if request_body:

        print(f'Type of request body received is: {type(request_body)}')

        if request_body:

            if r_content_type == 'application/json':

                try:
                    _request_body_str = request_body.decode('utf-8')
                except (UnicodeDecodeError, AttributeError):
                    print('\nFailed to decode request body (Request body was unexpected type)!', file=sys.stderr)
                    return
                print('Request body (decoded string is:)')
                print(_request_body_str)

                # request_body_dict = json.loads(_request_body_str)
                # print('Request body given is:')
                # pprint(request_body_dict)
        else:
            print('Content Type was not application/json, will print whatever body received')
            # print(pformat(request_body))
            print(request_body)

    request_headers = request.headers

    if request_headers:
        print('Request Headers given as:')
        pprint(request_headers)

    # return {'name': 'neel'}
    # make_response()
    # return make_response('success')

    return make_response(jsonify(response_data), 200)


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


@app.route('/matrixevents', methods=['POST'])
def handle():

    return make_response(jsonify({'success': True}), 200)


@app.route('/scbi/v2/actions', methods=['GET', 'POST'])
def scbi_v2_actions():

    _request_path = request.path
    request_status = f'{request.method} request received on path: {_request_path}'
    print(request_status)
    """ Example
    POST request received on path: /scbi/v2/actions
    """
    response_data = {'status': request_status}

    if request.query_string:
        rqs = request.query_string
        print(f'Query string in request is:\n{rqs}')
        """ Example:
        b'op=scbi.shareWebReport&org=RENTALSG&propid=c986a87de1ec42718ed68c69af282022&pid=9a20c722cd364be1a0b3260449764f4b'
        """

    r_content_type = request.content_type
    print(f'Content type of request is: {r_content_type}')

    request_headers = request.headers

    if request_headers:
        print('Request Headers given as:')
        pprint(dict(request_headers))
    else:
        print('No headers given in this request (cannot be!)')

    # request_body = request.data
    request_body = request.data

    if request_body:

        print(f'Type of request body received is: {type(request_body)}')

        print('\nRequest data (raw format) is:')
        print(request_body)

        if r_content_type == 'application/json':

            try:
                _request_body_str = request_body.decode('utf-8')
            except (UnicodeDecodeError, AttributeError):
                print('\nFailed to decode request body (Request body was unexpected type)!', file=sys.stderr)
                return
            print('Request body (decoded string is:)')
            print(_request_body_str)

            # request_body_dict = json.loads(_request_body_str)
            # print('Request body given is:')
            # pprint(request_body_dict)
        else:
            print('Content Type was not application/json, will print whatever body received')
            # print(pformat(request_body))
            print(request_body)

    # return {'name': 'neel'}
    # make_response()
    # return make_response('success')

    return make_response(jsonify(response_data), 200)
