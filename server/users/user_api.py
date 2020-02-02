from flask import make_response, jsonify
from http import HTTPStatus

from server import db
from server.utils import encode_JWT, get_JWT_from_cookie, error_message, hash_password
from server.config import JWT_COOKIE_NAME
from server.users.abstract_user_api import AbstractUserAPI
from server.models.validators import login_validator, create_user_validator, set_user_data_validator, \
    set_user_password_validator, set_user_groups_validator
from server.models.entity import User, Group
from server.models.to import UserDetailsTO, UserInfoTO


class UserAPI(AbstractUserAPI):
    def __init__(self):
        super().__init__()
        self.version = 'v1'

    @staticmethod
    def login(request):
        form = request.json or {}
        errors = login_validator.validate(form)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)

        pass_hash = hash_password(form['password'])
        user = User.query.filter_by(username=form['username'], password_hash=pass_hash).first()
        if user is None:
            return error_message('Wrong username or password!', HTTPStatus.BAD_REQUEST)
        user = UserDetailsTO(user)

        encoded_jwt = user.get_jwt()

        # jsonify({JWT_COOKIE_NAME: encoded_jwt})
        resp = make_response()
        resp.status_code = HTTPStatus.OK
        resp.set_cookie(JWT_COOKIE_NAME, encoded_jwt)

        return resp

    @staticmethod
    def logout(request):
        resp = make_response()
        resp.status_code = HTTPStatus.OK
        resp.delete_cookie(JWT_COOKIE_NAME)
        return resp

    @staticmethod
    def refresh_token(request):
        users_jwt = get_JWT_from_cookie()
        if not users_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)
        if 'exp' in users_jwt:
            users_jwt.pop('exp')

        encoded = encode_JWT(users_jwt)

        # jsonify({JWT_COOKIE_NAME: encoded})
        resp = make_response()
        resp.status_code = HTTPStatus.OK
        resp.set_cookie(JWT_COOKIE_NAME, encoded)
        
        return resp

    @staticmethod
    def register(request):
        user_jwt = get_JWT_from_cookie()
        if not user_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)

        form = request.json or {}
        form['licence_id'] = user_jwt['licence_id']
        errors = create_user_validator.validate(form)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)
        
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
        users_jwt = get_JWT_from_cookie()
        if not users_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)

        transport_object = UserInfoTO
        if users_jwt.get('is_admin', False):
            transport_object = UserDetailsTO

        users = User.query.filter_by(licence_id=users_jwt['licence_id']).all()
        users_to = transport_object.from_list(users)
        users_to = [user.to_dict() for user in users_to]

        resp = make_response(jsonify({'users': users_to}))
        resp.status_code = HTTPStatus.OK

        return resp

    @staticmethod
    def user_details_GET(request, user_id):
        users_jwt = get_JWT_from_cookie()
        if not users_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)

        if not users_jwt['is_admin'] and users_jwt['id'] != user_id:
            return error_message('Forbidden', status=HTTPStatus.FORBIDDEN)

        user = User.query.filter_by(id=user_id, licence_id=users_jwt['licence_id']).first()
        if not user:
            return error_message('User not found!', status=HTTPStatus.NOT_FOUND)
        user_to = UserDetailsTO(user)
        
        resp = make_response(jsonify({'user': user_to.to_dict()}))
        resp.status_code = HTTPStatus.FOUND
        
        return resp

    @staticmethod
    def user_details_PUT(request, user_id):
        users_jwt = get_JWT_from_cookie()
        if not users_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)

        if not users_jwt['is_admin']:
            return error_message('Forbidden', status=HTTPStatus.FORBIDDEN)

        user = User.query.filter_by(id=user_id, licence_id=users_jwt['licence_id']).first()
        if not user:
            return error_message('User not found!', status=HTTPStatus.NOT_FOUND)

        form = request.json or {}
        errors = set_user_data_validator.validate(form)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)

        user_to = UserDetailsTO(user)

        errors = user_to.set_data(form)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)

        errors = user_to.update_model(user)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)

        db.session.commit()

        resp = make_response(jsonify(user_to.to_dict()))
        resp.status_code = HTTPStatus.OK

        return resp

    @staticmethod
    def user_details_DELETE(request, user_id):
        users_jwt = get_JWT_from_cookie()
        if not users_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)

        if not users_jwt['is_admin'] or users_jwt['id'] == user_id:
            return error_message('Forbidden', status=HTTPStatus.FORBIDDEN)

        user = User.query.filter_by(id=user_id, licence_id=users_jwt['licence_id']).first()
        if not user:
            return error_message('User not found!', status=HTTPStatus.NOT_FOUND)

        db.session.delete(user)
        db.session.commit()
        resp = make_response()
        resp.status_code = HTTPStatus.NO_CONTENT
        return resp

    @staticmethod
    def set_user_password(request):
        users_jwt = get_JWT_from_cookie()
        if not users_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)

        form = request.json or {}
        errors = set_user_password_validator.validate(form)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)

        user = User.query.filter_by(id=users_jwt['id']).first()
        if not user:
            return error_message('User not found!', status=HTTPStatus.NOT_FOUND)

        old_hash = hash_password(form['old_password'])
        if old_hash != user.password_hash:
            return error_message('Wrong password!', status=HTTPStatus.BAD_REQUEST)

        new_hash = hash_password(form['new_password'])
        user.password_hash = new_hash
        db.session.commit()

        resp = make_response()
        resp.status_code = HTTPStatus.OK

        return resp

    @staticmethod
    def set_user_avatar(request, user_id):
        return error_message('Not implemented yet!', status=HTTPStatus.NOT_FOUND)

    @staticmethod
    def set_user_groups(request, user_id):
        users_jwt = get_JWT_from_cookie()
        if not users_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)

        if not users_jwt['is_admin']:
            return error_message('Forbidden', status=HTTPStatus.FORBIDDEN)

        form = request.json or []
        errors = set_user_groups_validator.validate({'groups': form})
        if errors:
            return error_message(str(errors), status=HTTPStatus.BAD_REQUEST)

        user = User.query.filter_by(id=user_id, licence_id=users_jwt['licence_id']).first()
        if not user:
            return error_message('User does not exist!', status=HTTPStatus.BAD_REQUEST)

        groups = Group.query.filter_by(licence_id=users_jwt['licence_id']).filter(Group.name.in_(form)).all()
        user.groups.extend(groups)

        db.session.commit()

        user_to = UserDetailsTO(user)

        resp = make_response(jsonify(user_to.to_dict()))
        resp.status_code = HTTPStatus.OK

        return resp
