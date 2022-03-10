import os
import logging

# import yaml

import definitions

# region Data Definition: Checker functions
MODEL_CHECKER_DATA_RETURN = definitions.CHECKER_MODEL_DATA_RETURN
CHECKER_ATTR_TEXT = definitions.CHECKER_ATTR_TEXT
CHECKER_ATTR_STATUS = definitions.CHECKER_ATTR_STATUS
CHECKER_ATTR_ERROR = definitions.CHECKER_ATTR_STATUS
# endregion


# def load_data_from_yaml_file(filepath: str) -> dict:
#     """"""
#
#     print('Loading data from yaml file at given path:')
#     print(filepath)
#
#     if not os.path.isfile(filepath):
#         raise FileNotFoundError(f'There is no such file: {filepath}')
#
#     with open(filepath) as f:
#         data = yaml.safe_load(f)
#
#         print('Data loaded from yaml file as dict.')
#
#         return data

def _get_std_log_level_from_input(log_level_input: str) -> int:

    input_all_caps = log_level_input.upper()

    log_level_by_input = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR
    }

    if input_all_caps in log_level_by_input:
        return log_level_by_input[input_all_caps]

    return logging.CRITICAL


def get_logger_for_module(module_name: str, log_level_input: str):

    _std_log_level = _get_std_log_level_from_input(log_level_input)

    module_logger = logging.getLogger(module_name)

    if module_logger.hasHandlers():
        module_logger.setLevel(_std_log_level)
        return module_logger

    logging.basicConfig(level=_std_log_level)

    module_logger = logging.getLogger(module_name)

    return module_logger
def _check_string_is_valid(value: any) -> MODEL_CHECKER_DATA_RETURN:

    data_return = MODEL_CHECKER_DATA_RETURN.copy()

    type_value = type(value)
    if type_value != str:
        data_return[CHECKER_ATTR_TEXT] = f'given type: {type_value.__name__}'
        return data_return

    attr_value_status = f'value is: {value}'

    if value == '' or value == 'null':
        data_return[CHECKER_ATTR_TEXT] = attr_value_status
        return data_return

    data_return['status'] = True
    data_return['text'] = 'given valid string'
    return data_return


def _check_boolean_is_valid(value: any) -> MODEL_CHECKER_DATA_RETURN:

    data_return = MODEL_CHECKER_DATA_RETURN.copy()

    type_value = type(value)
    if type_value != bool:
        data_return[CHECKER_ATTR_TEXT] = f'given value has type: {type_value.__name__}'
        return data_return

    data_return['status'] = True
    data_return['text'] = 'given value is a valid boolean'
    return data_return


def _check_integer_is_valid(value: any) -> MODEL_CHECKER_DATA_RETURN:

    data_return = MODEL_CHECKER_DATA_RETURN.copy()

    type_value = type(value)
    if type_value != int:
        data_return[CHECKER_ATTR_TEXT] = f'given value has type: {type_value.__name__}'
        return data_return

    data_return['status'] = True
    data_return['text'] = 'given value is a valid integer'
    return data_return


def check_dict_is_valid(value: any) -> MODEL_CHECKER_DATA_RETURN:

    data_return = MODEL_CHECKER_DATA_RETURN.copy()

    type_value = type(value)
    if type_value != dict:
        data_return[CHECKER_ATTR_TEXT] = f'given value has type: {type_value.__name__}'
        return data_return

    if not value:
        data_return[CHECKER_ATTR_TEXT] = 'given value is empty dictionary'
        return data_return

    data_return[CHECKER_ATTR_STATUS] = True
    data_return[CHECKER_ATTR_TEXT] = 'given value is valid dictionary'
    return data_return


def _check_list_is_valid(value: any) -> MODEL_CHECKER_DATA_RETURN:

    data_return = MODEL_CHECKER_DATA_RETURN.copy()

    type_value = type(value)
    if type_value != list:
        data_return[CHECKER_ATTR_TEXT] = f'given value has type: {type_value.__name__}'
        return data_return

    if not value:
        data_return[CHECKER_ATTR_TEXT] = 'given value is empty list'
        return data_return

    data_return[CHECKER_ATTR_STATUS] = True
    data_return[CHECKER_ATTR_TEXT] = 'given value is valid list'
    return data_return


def extract_attr_from_data(data: dict, data_name: str, attr_name: str, exp_type: type) -> dict:

    data_return = {
        'value': None,
        'text': 'default',
        'error': False
    }

    if attr_name not in data:
        data_return['text'] = f'{attr_name} not given in {data_name}.'
        return data_return
    attr_value = data[attr_name]

    data_return['text'] = f'Extracted "{attr_name}" from {data_name}'

    if exp_type is str:
        _check_valid_resp = _check_string_is_valid(attr_value)
        _valid = _check_valid_resp['status']
        _valid_status = _check_valid_resp['text']
        if _valid is False:
            data_return['error'] = True
            data_return['text'] += f' but {_valid_status} (Expected string)'
            return data_return
        data_return['value'] = attr_value
        data_return['text'] += f' and checked it is a valid {exp_type.__name__} value'
        return data_return

    if exp_type is dict:
        _check_valid_resp = check_dict_is_valid(attr_value)
        _valid = _check_valid_resp['status']
        _valid_status = _check_valid_resp['text']
        if _valid is False:
            data_return['error'] = True
            data_return['text'] += f' but {_valid_status} (Expected dictionary)'
            return data_return
        data_return['value'] = attr_value
        data_return['text'] = f' and checked it is a valid {exp_type.__name__} value'
        return data_return

    if exp_type is int:
        _check_valid_resp = _check_integer_is_valid(attr_value)
        _valid = _check_valid_resp['status']
        _valid_status = _check_valid_resp['text']
        if _valid is False:
            data_return['error'] = True
            data_return['text'] += f' but {_valid_status} (Expected {exp_type.__name__})'
            return data_return
        data_return['value'] = attr_value
        data_return['text'] += f' and checked it is a valid {exp_type.__name__} value'
        return data_return

    if exp_type is list:
        _check_valid_resp = _check_list_is_valid(attr_value)
        _valid = _check_valid_resp['status']
        _valid_status = _check_valid_resp['text']
        if _valid is False:
            data_return['error'] = True
            data_return['text'] += f' but {_valid_status} (Expected {exp_type.__name__})'
            return data_return
        data_return['value'] = attr_value
        data_return['text'] = f' and checked it is a valid {exp_type.__name__} value'
        return data_return

    if exp_type is bool:
        _check_valid_resp = _check_boolean_is_valid(attr_value)
        _valid = _check_valid_resp['status']
        _valid_status = _check_valid_resp['text']
        if _valid is False:
            data_return['error'] = True
            data_return['text'] += f' but {_valid_status} (Expected {exp_type.__name__})'
            return data_return
        data_return['value'] = attr_value
        data_return['text'] += f' and checked it is a valid {exp_type.__name__} value'
        return data_return

    # TODO: Handle other types as required
    raise Exception('Not Implemented')
