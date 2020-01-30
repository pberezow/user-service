from flask import make_response, jsonify
from http import HTTPStatus

from server import db
from server.utils import encode_JWT, decode_JWT, get_JWT_from_cookie, error_message, hash_password
from server.config import JWT_COOKIE_NAME
from server.users.abstract_user_api import AbstractUserAPI
from server.models.validators import login_validator, create_user_validator
from server.models.entity import User
from server.models.to import UserDetailsTO


class UserAPI(AbstractUserAPI):
    def __init__(self):
        super().__init__()
        self.version = 'v1'

    @staticmethod
    def login(request):
        errors = login_validator.validate(request.json)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)

        pass_hash = hash_password(request.json['password'])
        user = User.query.filter_by(username=request.json['username'], password_hash=pass_hash).first()
        if user is None:
            return error_message('Wrong username or password!', HTTPStatus.BAD_REQUEST)
        user = UserDetailsTO(user)

        encoded_jwt = user.get_jwt()

        resp = make_response(jsonify({JWT_COOKIE_NAME: encoded_jwt}))
        resp.status_code = HTTPStatus.OK
        resp.set_cookie(JWT_COOKIE_NAME, encoded_jwt)

        return resp

    @staticmethod
    def refresh_token(request):
        users_jwt = get_JWT_from_cookie()
        if 'exp' in users_jwt:
            users_jwt.pop('exp')

        encoded = encode_JWT(users_jwt)
        
        resp = make_response(jsonify({JWT_COOKIE_NAME: encoded}))
        resp.status_code = HTTPStatus.OK
        resp.set_cookie(JWT_COOKIE_NAME, encoded)
        
        return resp

    @staticmethod
    def register(request):
        errors = create_user_validator.validate(request.json)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)
        
        form = request.json
        pass_hash = hash_password(form['password'])
        form.pop('password')
        form['password_hash'] = pass_hash
        try:
            new_user = User(**form)
            db.session.add(new_user)
            db.session.commit()
        except:
            return error_message('Error while creating new user!', HTTPStatus.INTERNAL_SERVER_ERROR)

        user_to = UserDetailsTO(new_user)
        return jsonify(user_to.to_dict()), HTTPStatus.CREATED

    @staticmethod
    def users_list(request):
        users = User.query.all()
        users_to = UserDetailsTO.from_list(users)
        users_to = [user.to_dict() for user in users_to]
        
        resp = make_response(jsonify({'users': users_to}))
        resp.status_code = HTTPStatus.OK
        
        return resp

    @staticmethod
    def user_details_GET(request, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return error_message('User not found!', status=HTTPStatus.NOT_FOUND)
        user_to = UserDetailsTO(user)
        
        resp = make_response(jsonify({'user': user_to.to_dict()}))
        resp.status_code = HTTPStatus.FOUND
        
        return resp

    @staticmethod
    def user_details_PUT(request, user_id):
        raise NotImplementedError()

    @staticmethod
    def user_details_DELETE(request, user_id):
        raise NotImplementedError()

    @staticmethod
    def set_user_avatar(request, user_id):
        return error_message('Not implemented yet!', status=HTTPStatus.NOT_FOUND)

    @staticmethod
    def set_user_groups(request, user_id):
        raise NotImplementedError()
