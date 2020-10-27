import json
from pprint import pprint
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    request_status = f'{request.method} request received on index.'
    print(request_status)
    response_data = {'status': request_status}
    
    request_body = request.data
    if request_body:
        request_body_json_string = request_body.decode('utf-8')
        request_body_dict = json.loads(request_body_json_string)
        response_data['data'] = request_body_dict
        print('Request body given is:')
        pprint(request_body_dict)

    return make_response(jsonify(response_data), 200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
