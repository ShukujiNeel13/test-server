import base64
import json
import os.path
from pprint import pformat

SAMPLE_AUTH_RESPONSE = {
    'code': None,
    'data': {'access_token': 'eyJraWQiOiJRZTlQUXUzYWxcL2cyTzltOHRWMkRHejdkV3NWNjF0WHBVRU9mYnJkTmo4az0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3YjM1ZnEwM3Nlb2VrNXM3b3ZmNjBqMml2NyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoibWF0cml4LnNvbHV0aW9uc1wvc29sdXRpb25zLm5vdGlmeSIsImF1dGhfdGltZSI6MTY0Njg4MzI4MiwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoZWFzdC0xLmFtYXpvbmF3cy5jb21cL2FwLXNvdXRoZWFzdC0xX0pKMVBKdE9jViIsImV4cCI6MTY0Njg4Njg4MiwiaWF0IjoxNjQ2ODgzMjgyLCJ2ZXJzaW9uIjoyLCJqdGkiOiJiM2Y3OTBmZi0xOTljLTQzOGMtYjY4Ny1kMzZkYWRjYWU4MGIiLCJjbGllbnRfaWQiOiI3YjM1ZnEwM3Nlb2VrNXM3b3ZmNjBqMml2NyJ9.Zb_cAWrtR9baPrguKdLBy9QMnmE4mT3zruIgv6cA7yFwlbRg8-R62_PUF_Mu_g35lmdB-dDeqanDqz_PjO3ORIDmz0W2mX1XpNmjKWNTHDN_cBGFleabwzIEpregtIkcy5FbZc4LGfCb5kYSSS-NrmZQtnJOTFe2Un9eYT4kSz_rTPYeVKIPyy_AvwxrwnOAmHGSJ-bYt3K10Gl9PDQc3a5i4j39ykBci3tVcVihvPTNP2X-KQcaiHAZ3iMNyO-91eQ0L_VJKlAZgHl1b8hnwbincECLfjEk5Wlh6xXhDIqa4K47rW24-g1ZxDHY8RiFQZ9EGoT3iLI49LSARMiSBg',
             'expires_in': 3600,
             'token_type': 'Bearer'},
    'error': False,
    'message': 'Obtained credential data for client'
}

TOKEN_HEADER = 'eyJraWQiOiJRZTlQUXUzYWxcL2cyTzltOHRWMkRHejdkV3NWNjF0WHBVRU9mYnJkTmo4az0iLCJhbGciOiJSUzI1NiJ9'
TOKEN_PAYLOAD = 'eyJzdWIiOiI3YjM1ZnEwM3Nlb2VrNXM3b3ZmNjBqMml2NyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoibWF0cml4LnNvbHV0aW9uc1wvc29sdXRpb25zLm5vdGlmeSIsImF1dGhfdGltZSI6MTY0Njg4MzI4MiwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoZWFzdC0xLmFtYXpvbmF3cy5jb21cL2FwLXNvdXRoZWFzdC0xX0pKMVBKdE9jViIsImV4cCI6MTY0Njg4Njg4MiwiaWF0IjoxNjQ2ODgzMjgyLCJ2ZXJzaW9uIjoyLCJqdGkiOiJiM2Y3OTBmZi0xOTljLTQzOGMtYjY4Ny1kMzZkYWRjYWU4MGIiLCJjbGllbnRfaWQiOiI3YjM1ZnEwM3Nlb2VrNXM3b3ZmNjBqMml2NyJ9'
TOKEN_SIGNATURE = 'Zb_cAWrtR9baPrguKdLBy9QMnmE4mT3zruIgv6cA7yFwlbRg8-R62_PUF_Mu_g35lmdB-dDeqanDqz_PjO3ORIDmz0W2mX1XpNmjKWNTHDN_cBGFleabwzIEpregtIkcy5FbZc4LGfCb5kYSSS-NrmZQtnJOTFe2Un9eYT4kSz_rTPYeVKIPyy_AvwxrwnOAmHGSJ-bYt3K10Gl9PDQc3a5i4j39ykBci3tVcVihvPTNP2X-KQcaiHAZ3iMNyO-91eQ0L_VJKlAZgHl1b8hnwbincECLfjEk5Wlh6xXhDIqa4K47rW24-g1ZxDHY8RiFQZ9EGoT3iLI49LSARMiSBg'

ACCESS_TOKEN = f'{TOKEN_HEADER}.{TOKEN_PAYLOAD}.{TOKEN_SIGNATURE}'

# Step 1 ensure the token has 3 sections separated by "."


# region Utils (In order of steps)
def _check_jwt_token_structure_valid(jwt_token: str) -> dict:

    response_data = {
        'status': False,
        'message': 'Structure invalid',
        'token_sections_by_name': None
    }

    _separating_char = '.'
    required_no_of_sections = 3

    _invalid_status_text = f'token must contain {required_no_of_sections} sections separated by {_separating_char}'

    if _separating_char not in jwt_token:
        response_data['message'] += f' ({_invalid_status_text})'
        return response_data

    _token_sections = jwt_token.split('.')
    no_of_sections = len(_token_sections)

    if no_of_sections != 3:
        response_data['message'] += f' ({_invalid_status_text})'
        return response_data

    token_sections_by_name = {
        'header': _token_sections[0],
        'payload': _token_sections[1],
        'signature': _token_sections[2]
    }

    response_data['token_sections_by_name'] = token_sections_by_name

    response_data['status'] = True
    response_data['message'] = 'Structure valid'
    return response_data


def _check_jwt_signature_valid(b64_encoded_signature: str) -> dict:
    """
    The JWT signature is a hashed combination of the header and the payload

    (A Key is used to sign this)

    :param b64_encoded_signature:
    :return:
    """

    response_data = {
        'status': False,
        'message': 'Signature invalid'
    }

    _key = '?'
    _invalid_status_text = f'JWT signature must be key-hashed combination of JWT Header and JWT Payload sections'

    decoded_signature = base64.b64decode(b64_encoded_signature)

    invalid = True
    if invalid:
        response_data['message'] += f' ({_invalid_status_text})'
        return response_data

    response_data['status'] = True
    response_data['message'] = 'JWT signature section is valid'
    return response_data


# TODO: Get the header from the unhased Signature?
def _check_header_kid_matches_key(kid: str, kid_alg: str = 'RS256', json_filepath_jwt_keys: str = None) -> dict:
    """
    Compare the local key ID (kid) to the public kid.

    :param header_kid:
    :param algorithm:
    :param match_how:
    :return:
    """

    response_data = {
        'status': False,
        'message': 'default'
    }

    # region Get keys data from the public jwt keys json file
    _file_data_name = 'public jwt keys json file'

    get_data_response = _get_data_from_jwt_keys_json_file(json_filepath_jwt_keys)
    json_file_data = get_data_response['data']
    get_json_file_message = get_data_response['message']

    if not json_file_data:
        response_data['message'] = f'Failed to get data from {_file_data_name} ({get_json_file_message})'
        return response_data

    if 'keys' not in json_file_data:
        response_data['message'] = f'Required attribute: "keys" missing in {_file_data_name}'
        return response_data
    # endregion

    list_of_keys_data = json_file_data['keys']

    # region Ensure keys in data is list
    _type_keys_data = type(list_of_keys_data)

    if _type_keys_data is not list:
        response_data['message'] = f'"keys" in {_file_data_name} must be list (but found: {_type_keys_data.__name__}'
        return response_data
    # endregion

    no_of_keys_data = len(list_of_keys_data)

    if no_of_keys_data == 1:
        key_data = list_of_keys_data[0]

    else:
        # Group by "alg"

    _group_by_alg_resp = _group_jwt_public_keys_by_attribute(
        list_of_keys_data,
        attr_name='alg',
        attr_value=kid_alg
    )

    _key = '?'
    _invalid_status_text = f'Key ID in JWT header section must match the public key id'

    invalid = True
    if invalid:
        response_data['message'] += f' ({_invalid_status_text})'
        return response_data

    response_data['status'] = True
    response_data['message'] = 'JWT signature section is valid'
    return response_data


def _group_jwt_public_keys_by_attribute(keys_data: list, attr_name: str, attr_value: str) -> dict:

    response_data = {
        'data': None,
        'message': 'default'
    }

    no_of_keys_data = len(keys_data)

    if no_of_keys_data == 1:
        key_data = keys_data[0]
    else:
        for key_data in keys_data:


    return response_data


def _get_data_from_jwt_keys_json_file(json_filepath: str = None) -> dict:

    response_data = {
        'data': None,
        'message': 'default'
    }

    if json_filepath is None:
        parent_dir_abs_path = os.path.dirname(os.path.abspath(__name__))
        json_filepath = f'{parent_dir_abs_path}/_public_jwt_keys.json'

    with open(json_filepath, mode='r') as f:
        try:
            keys_data = json.load(f)
        except Exception as err:
            _err_type = type(err).__name__
            _err_text = str(err)

            err_info = f'{_err_type} loading data from JSON file ({_err_text})'
            response_data['message'] = err_info

            return response_data

        response_data['data'] = keys_data

# endregion


def check_jwt_valid(jwt_token: str = None) -> dict:

    response_data = {
        'status': False,
        'code': 'TOKEN_INVALID',
        'error': 'False',
        'message': 'default'
    }

    # region Check structure valid
    _check_structure_resp = _check_jwt_token_structure_valid(jwt_token)
    structure_valid = _check_structure_resp['status']
    check_structure_message = _check_structure_resp['message']

    if structure_valid is False:
        response_data['message'] = check_structure_message
        return response_data
    # endregion

    token_sections_by_name = _check_structure_resp['token_sections_by_name']

    token_signature_b64_string = token_sections_by_name['signature']

    # region Check signature section valid
    _check_signature_resp = _check_jwt_signature_valid(token_signature_b64_string)
    structure_valid = _check_structure_resp['status']
    check_structure_message = _check_structure_resp['message']

    if structure_valid is False:
        response_data['message'] = check_structure_message
        return response_data
    # endregion

    token_header_b64_string = token_sections_by_name['header']

    # region Check header key id matches public key id
    _check_signature_resp = _check_header_kid_matches_key(token_header_b64_string)
    structure_valid = _check_structure_resp['status']
    check_structure_message = _check_structure_resp['message']

    if structure_valid is False:
        response_data['message'] = check_structure_message
        return response_data
    # endregion


if __name__ == '__main__':
    access_token = ...
    response = check_jwt_valid(access_token)
    print(f'Process complete. Response is:\n{pformat(response)}')



