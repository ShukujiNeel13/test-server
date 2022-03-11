import base64
import json
import os.path
from time import time
from pprint import pformat

import jwt

import utils

SAMPLE_AUTH_RESPONSE = {
    'code': None,
    'data': {
        'access_token': 'eyJraWQiOiJRZTlQUXUzYWxcL2cyTzltOHRWMkRHejdkV3NWNjF0WHBVRU9mYnJkTmo4az0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3YjM1ZnEwM3Nlb2VrNXM3b3ZmNjBqMml2NyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoibWF0cml4LnNvbHV0aW9uc1wvc29sdXRpb25zLm5vdGlmeSIsImF1dGhfdGltZSI6MTY0Njg4MzI4MiwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoZWFzdC0xLmFtYXpvbmF3cy5jb21cL2FwLXNvdXRoZWFzdC0xX0pKMVBKdE9jViIsImV4cCI6MTY0Njg4Njg4MiwiaWF0IjoxNjQ2ODgzMjgyLCJ2ZXJzaW9uIjoyLCJqdGkiOiJiM2Y3OTBmZi0xOTljLTQzOGMtYjY4Ny1kMzZkYWRjYWU4MGIiLCJjbGllbnRfaWQiOiI3YjM1ZnEwM3Nlb2VrNXM3b3ZmNjBqMml2NyJ9.Zb_cAWrtR9baPrguKdLBy9QMnmE4mT3zruIgv6cA7yFwlbRg8-R62_PUF_Mu_g35lmdB-dDeqanDqz_PjO3ORIDmz0W2mX1XpNmjKWNTHDN_cBGFleabwzIEpregtIkcy5FbZc4LGfCb5kYSSS-NrmZQtnJOTFe2Un9eYT4kSz_rTPYeVKIPyy_AvwxrwnOAmHGSJ-bYt3K10Gl9PDQc3a5i4j39ykBci3tVcVihvPTNP2X-KQcaiHAZ3iMNyO-91eQ0L_VJKlAZgHl1b8hnwbincECLfjEk5Wlh6xXhDIqa4K47rW24-g1ZxDHY8RiFQZ9EGoT3iLI49LSARMiSBg',
        'expires_in': 3600,
        'token_type': 'Bearer'
    },
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
        'token_sections_by_name': None,
        'jwtVerifyStepNumber': 1
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


def _check_header_kid_matches_any_public_key(local_kid: str, kid_alg: str = 'RS256', json_filepath_jwt_keys: str = None) -> dict:
    """
    Compare the local key ID (kid) to the public kid.

    :param kid:
    :param kid_alg:
    :param json_filepath_jwt_keys:
    :return:
    """

    response_data = {
        'status': False,
        'message': 'default',
        'jwtVerifyStepNumber': 3,
        'public_key': None
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

    # region If no of keys in public jwt keys json file is 1 - do matching
    if no_of_keys_data == 1:
        key_data = list_of_keys_data[0]
        _get_kid_resp = utils.extract_attr_from_data(key_data, 'key data', 'kid', str)
        public_kid = _get_kid_resp['value']
        get_kid_text = _get_kid_resp['text']

        if public_kid is None:
            response_data['message'] = f'Failed to get kid from {_file_data_name} ({get_kid_text})'
            return response_data

        if local_kid == public_kid:
            response_data['status'] = True
            response_data['message'] = 'Local kid matched public kid'
        else:
            response_data['message'] = 'Local kid did not match public kid'

        return response_data
    # endregion

    # region Get public keys data matching "alg" of given key - return if none match
    _get_jwt_public_keys_matching_alg_resp = _get_jwt_public_keys_matching_alg(
        list_of_keys_data,
        alg_value=kid_alg
    )

    keys_data_matching_alg = _get_jwt_public_keys_matching_alg_resp['data']
    get_jwt_public_keys_matching_alg_message = _get_jwt_public_keys_matching_alg_resp['message']

    if keys_data_matching_alg is None:
        response_data['message'] = get_jwt_public_keys_matching_alg_message
        return response_data
    # endregion

    if len(keys_data_matching_alg) == 1:
        key_data = keys_data_matching_alg[0]

        _get_kid_resp = utils.extract_attr_from_data(key_data, 'public key data', 'kid', str)
        public_kid = _get_kid_resp['value']
        get_kid_text = _get_kid_resp['text']

        if public_kid is None:
            response_data['message'] = f'Failed to get kid from {_file_data_name} ({get_kid_text})'
            return response_data

        if local_kid == public_kid:
            response_data['status'] = True
            response_data['message'] = 'Local kid matched a public kid'

            # region Get public key from public kid data
            _get_public_key_resp = utils.extract_attr_from_data(
                key_data,
                'public key data',
                'n',
                str
            )

            token_public_key = _get_public_key_resp['value']
            get_public_key_text = _get_public_key_resp['text']

            if token_public_key is None:
                response_data['message'] = get_public_key_text
                return response_data

            # endregion
            response_data['public_key'] = token_public_key

        else:
            response_data['message'] = 'Local kid did not match public kid'

        return response_data
    else:
        for key_data in keys_data_matching_alg:

            _get_kid_resp = utils.extract_attr_from_data(key_data, 'key data', 'kid', str)
            public_kid = _get_kid_resp['value']
            get_kid_text = _get_kid_resp['text']

            if public_kid is None:
                print(f'Failed to get kid from {_file_data_name} ({get_kid_text})')
                continue

            if local_kid == public_kid:
                response_data['status'] = True
                response_data['message'] = 'Local kid matched a public kid'

                # region Get public key from public kid data
                _get_public_key_resp = utils.extract_attr_from_data(
                    key_data,
                    'public key data',
                    'n',
                    str
                )

                token_public_key = _get_public_key_resp['value']
                get_public_key_text = _get_public_key_resp['text']

                if token_public_key is None:
                    response_data['message'] = get_public_key_text
                    return response_data

                # endregion
                response_data['public_key'] = token_public_key

                return response_data
        response_data['message'] = f'local kid did not match any of the public kid having alg = {kid_alg}'
        return response_data


def _get_jwt_public_keys_matching_alg(keys_data: list, alg_value: str = 'RS256') -> dict:

    response_data = {
        'data': None,
        'message': 'default'
    }

    no_of_keys_data = len(keys_data)

    if no_of_keys_data == 1:
        key_data = keys_data[0]
        _get_alg_resp = utils.extract_attr_from_data(key_data, 'public key data', 'alg', str)

        alg = _get_alg_resp['value']
        get_alg_text = _get_alg_resp['text']

        if alg is None:
            response_data['message'] = f'This public key data is invalid ({get_alg_text})'
            return response_data

        if alg == alg_value:
            response_data['data'] = key_data
            response_data['message'] = f'Public key data found with alg = {alg_value}'
        else:
            response_data['message'] = f'No keys found with alg = {alg}'

        return response_data
    else:
        keys_data_matching_alg = [key_data for key_data in keys_data if key_data['alg'] == alg_value]

        if not keys_data_matching_alg:
            response_data['message'] = f'None of the keys data have alg = {alg_value}'
            return response_data

        response_data['data'] = keys_data_matching_alg
        response_data['message'] = f'Obtained keys data with alg = {alg_value}'
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
        return response_data


def _check_token_not_expired():
    ...


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
    # process_step_number = _check_structure_resp['jwtVerifyStepNumber']

    if structure_valid is False:
        response_data['message'] = f'Step 1 failed. {check_structure_message}'
        return response_data
    # endregion

    token_sections_by_name = _check_structure_resp['token_sections_by_name']

    # token_signature_b64_string = token_sections_by_name['signature']

    # region Check signature section valid
    # _check_signature_resp = _check_jwt_signature_valid(token_signature_b64_string)
    # signature_valid = _check_signature_resp['status']
    # check_signature_message = _check_signature_resp['message']
    #
    # if structure_valid is False:
    #     response_data['message'] = f'Step 2 failed. {check_signature_message}'
    #     return response_data
    # endregion

    token_header = token_sections_by_name['header']

    # region Decode token header
    _decoded_token_header_bytes = base64.b64decode(token_header)
    _decoded_token_header_data_json_string = _decoded_token_header_bytes.decode('utf-8')
    decoded_token_header_data = json.loads(_decoded_token_header_data_json_string)
    # endregion

    # region Get kid from decoded token header data
    _get_kid_resp = utils.extract_attr_from_data(
        decoded_token_header_data,
        'decoded jwt header',
        'kid',
        str
    )

    local_kid = _get_kid_resp['value']
    get_kid_text = _get_kid_resp['text']

    if local_kid is None:
        response_data['message'] = get_kid_text
        return response_data
    # endregion

    # region Get alg from decoded token header data
    _get_alg_resp = utils.extract_attr_from_data(
        decoded_token_header_data,
        'decoded jwt header',
        'alg',
        str
    )

    local_key_alg = _get_alg_resp['value']
    get_alg_text = _get_alg_resp['text']

    if local_key_alg is None:
        response_data['message'] = get_alg_text
        return response_data

    # endregion

    # region Check header key id matches public key id

    _check_header_key_id_valid_resp = _check_header_kid_matches_any_public_key(local_kid, local_key_alg)
    key_valid = _check_header_key_id_valid_resp['status']
    check_key_valid_message = _check_header_key_id_valid_resp['message']

    if key_valid is False:
        response_data['message'] = f'Step 3 failed. {check_key_valid_message}'
        return response_data

    # endregion
    token_public_key = _check_header_key_id_valid_resp['public_key']

    token_payload = token_sections_by_name['payload']

    # region Decode token payload
    _decoded_token_payload_bytes = base64.b64decode(token_payload)
    _decoded_token_payload_data_json_string = _decoded_token_payload_bytes.decode('utf-8')
    decoded_token_payload_data = json.loads(_decoded_token_payload_data_json_string)
    # endregion

    # region Get exp from decoded token payload data
    _get_exp_resp = utils.extract_attr_from_data(
        decoded_token_payload_data,
        'decoded jwt payload',
        'exp',
        int
    )

    token_exp = _get_exp_resp['value']
    get_exp_text = _get_exp_resp['text']

    if token_exp is None:
        response_data['message'] = get_exp_text
        return response_data

    # endregion

    curr_unix_time = int(time())

    if token_exp < curr_unix_time:
        response_data['message'] = 'Given token has already expired'
        return response_data

    # region Get token_use from decoded token payload data
    _get_token_use_resp = utils.extract_attr_from_data(
        decoded_token_payload_data,
        'decoded jwt payload',
        'token_use',
        str
    )

    token_use = _get_token_use_resp['value']
    get_token_use_text = _get_token_use_resp['text']

    if token_use is None:
        response_data['message'] = get_token_use_text
        return response_data

    # endregion

    if token_use != 'access':
        response_data['message'] = f'token_use in decoded token payload is: {token_use} (Required: "access")'
        return response_data

    # region Get iat from decoded token payload data
    _get_iat_resp = utils.extract_attr_from_data(
        decoded_token_payload_data,
        'decoded jwt payload',
        'iat',
        int
    )

    token_iat = _get_iat_resp['value']
    get_iat_text = _get_iat_resp['text']

    if token_iat is None:
        response_data['message'] = get_iat_text
        return response_data

    # endregion

    if token_iat > curr_unix_time:
        response_data['message'] = f'UNEXPECTED: iat in token payload is greater than current unix time'
        return response_data

    # region Get client_id from decoded token payload data
    _get_client_id_resp = utils.extract_attr_from_data(
        decoded_token_payload_data,
        'decoded jwt payload',
        'client_id',
        str
    )

    token_client_id = _get_client_id_resp['value']
    get_client_id_text = _get_client_id_resp['text']

    if token_client_id is None:
        response_data['message'] = get_client_id_text
        return response_data

    # endregion

    # TODO: Require client id to verify with token client id...

    # region Get scope from decoded token payload data
    _get_scope_resp = utils.extract_attr_from_data(
        decoded_token_payload_data,
        'decoded jwt payload',
        'scope',
        str
    )

    token_scope = _get_scope_resp['value']
    get_scope_text = _get_scope_resp['text']

    if token_scope is None:
        response_data['message'] = get_scope_text
        return response_data

    # endregion

    decode_jwt_response = _decode_jwt(token=jwt_token, public_key=token_public_key, alg=local_key_alg)

    decoded_jwt_data = decode_jwt_response['data']
    decoded_jwt_message = decode_jwt_response['message']

    if decoded_jwt_data is None:
        response_data['message'] = f'Failed to decode JWT token ({decoded_jwt_message})'
        return response_data

    # Match decoded jwt data with payload

    if decoded_jwt_data == decoded_token_payload_data:
        response_data['status'] = True
        response_data['code'] = 'SUCCESS'
        response_data['message'] = 'JWT token is valid'
        return response_data

    response_data['message'] = 'JWT token is invalid (signature matching failed)'
    return response_data


def _decode_jwt(token: str, public_key: str, alg: str) -> dict:

    response_data = {
        'data': None,
        'message': 'default'
    }

    try:
        response = jwt.decode(token, public_key, algorithms=[alg])
    except Exception as err:
        _err_type = type(err).__name__
        _err_text = str(err)
        err_info = f'{_err_type} decoding using JWT ({_err_text})'
        response_data['message'] = err_info
        return response_data

    response_data['data'] = response
    response_data['message'] = 'Decoded using JWT and given key and algorithm'
    return response_data


if __name__ == '__main__':
    access_token = 'eyJraWQiOiJRZTlQUXUzYWxcL2cyTzltOHRWMkRHejdkV3NWNjF0WHBVRU9mYnJkTmo4az0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3YjM1ZnEwM3Nlb2VrNXM3b3ZmNjBqMml2NyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoibWF0cml4LnNvbHV0aW9uc1wvc29sdXRpb25zLm5vdGlmeSIsImF1dGhfdGltZSI6MTY0NjkxMjcyOSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoZWFzdC0xLmFtYXpvbmF3cy5jb21cL2FwLXNvdXRoZWFzdC0xX0pKMVBKdE9jViIsImV4cCI6MTY0NjkxNjMyOSwiaWF0IjoxNjQ2OTEyNzI5LCJ2ZXJzaW9uIjoyLCJqdGkiOiJkOTNhZDM4YS1mODRhLTQ5YTAtOTRhMy00YTNhZTVjMmQ4NzEiLCJjbGllbnRfaWQiOiI3YjM1ZnEwM3Nlb2VrNXM3b3ZmNjBqMml2NyJ9.F_PEYoXXHKOAIFKUQe_jGjonI1TCYTu8lTssWGFp8KjS3YDD2W-979GBFzeOkCqF8RiKhHhVOqvwHpVI8NmmElS5e02cYmPMytmDAIYVkYtcLlOKglXNIuwcu1FmNycFA6J6HDbMHxeqY1KyNCIsqOAIXNEDPRYt1jmP_XXKQwRIjGKye4t9Y70vtB8rMX772lTHU2Sh_qLADnQSq1X_mYrw6m1TJGc4ro08EpFRBQTFsW0hB2EKLEuhwLtGHmDKXnyS1Az9_EXWegw03PeCbOCSfSGILymDlWqjAFZY3uVLOyGVHCkCIA3mzHpb1_QC3Zp7Df5Pihb22QLXCwEDfQ'
    response = check_jwt_valid(access_token)
    print(f'Process complete. Response is:\n{pformat(response)}')



