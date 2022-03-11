"""
Code in this module is adapted from:
Project: okta-jwks-to-pem (creator: jpf)
https://github.com/jpf/okta-jwks-to-pem
"""

import six
import base64
import struct

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def jwk_to_pem(jwk_object: dict):

    exponent = _base64_to_long(jwk_object['e'])
    modulus = _base64_to_long(jwk_object['n'])

    numbers = RSAPublicNumbers(exponent, modulus)

    public_key = numbers.public_key(backend=default_backend())

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    print('PEM is: \n')
    print(pem)


def _base64_to_long(data):
    if isinstance(data, six.text_type):
        data = data.encode("ascii")

    # urlsafe_b64decode will happily convert b64encoded data
    _d = base64.urlsafe_b64decode(bytes(data) + b'==')
    return _intarr2long(struct.unpack('%sB' % len(_d), _d))


def _intarr2long(arr):
    return int(''.join(["%02x" % byte for byte in arr]), 16)
