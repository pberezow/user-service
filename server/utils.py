import jwt
import hashlib
from datetime import datetime, timedelta
from http import HTTPStatus
from flask import jsonify, request
from server.config import PUBLIC_KEY, PRIVATE_KEY, SALT_PRE, SALT_POST, JWT_COOKIE_NAME


def hash_password(password):
    # sha256 - returns str with length = 64
    # sha512 - returns str with length = 128 
    utf_encoded_password = (SALT_PRE + password + SALT_POST).encode()
    return hashlib.sha256(utf_encoded_password).hexdigest()


# JWT construction - Base64(header) + '.' + Base64(data) + '.' + signature
def encode_JWT(payload):
    if not 'exp' in payload:
        payload['exp'] = datetime.utcnow() + timedelta(hours=4)
    return jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')


def decode_JWT(encoded_payload):
    try:
        return jwt.decode(encoded_payload, PUBLIC_KEY, algorithms='RS256')
    except:
        return {}


def get_JWT_from_cookie():
    encoded_jwt = request.cookies.get(JWT_COOKIE_NAME, None)
    if not encoded_jwt:
        return {}

    data = decode_JWT(encoded_jwt)  # .get('data', {})
    return data


def error_message(message, status=HTTPStatus.BAD_REQUEST, error_code=None):
    return jsonify({'error': message, 'code': error_code}), status
