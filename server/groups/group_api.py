from http import HTTPStatus
from flask import make_response, jsonify

from server import db
from server.groups.abstract_group_api import AbstractGroupAPI
from server.utils import error_message, get_JWT_from_cookie
from server.models.entity import Group
from server.models.validators import create_group_validator, set_group_data_validator
from server.models.to import GroupTO


class GroupAPI(AbstractGroupAPI):
    def __init__(self):
        super().__init__()
        self.version = 'v1'

    @staticmethod
    def add_group(request):
        users_jwt = get_JWT_from_cookie()
        if not users_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)

        if not users_jwt['is_admin']:
            return error_message('Forbidden', status=HTTPStatus.FORBIDDEN)

        form = request.json or {}
        form['licence_id'] = users_jwt['licence_id']
        errors = create_group_validator.validate(form)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)

        group = Group.query.filter_by(licence_id=form['licence_id'], name=form['name']).first()
        if group:
            return error_message(f'Group {form["name"]} already exists!', status=HTTPStatus.FORBIDDEN)  # status???

        group = Group(**form)
        db.session.add(group)
        db.session.commit()

        group_to = GroupTO(group)
        resp = make_response(jsonify(group_to.to_dict()))
        resp.status_code = HTTPStatus.CREATED

        return resp

    @staticmethod
    def get_all_groups(request):
        users_jwt = get_JWT_from_cookie()
        if not users_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)

        if not users_jwt['is_admin']:
            return error_message('Forbidden', status=HTTPStatus.FORBIDDEN)

        groups = Group.query.filter_by(licence_id=users_jwt['licence_id']).all()
        groups_to = GroupTO.from_list(groups)
        groups_to_list = [g.to_dict() for g in groups_to]

        resp = make_response(jsonify({'groups': groups_to_list}))
        resp.status_code = HTTPStatus.OK

        return resp

    @staticmethod
    def set_group(request, group_name):
        users_jwt = get_JWT_from_cookie()
        if not users_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)

        if not users_jwt['is_admin']:
            return error_message('Forbidden', status=HTTPStatus.FORBIDDEN)

        form = request.json or {}
        form['licence_id'] = users_jwt['licence_id']

        errors = set_group_data_validator.validate(form)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)

        group = Group.query.filter_by(licence_id=form['licence_id'], name=group_name).first()
        if not group:
            return error_message(f'Group {group_name} does not exist!', HTTPStatus.NOT_FOUND)

        group_to = GroupTO(group)
        errors = group_to.set_data(form)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)

        errors = group_to.update_model(group)
        if errors:
            return error_message(str(errors), HTTPStatus.BAD_REQUEST)

        db.session.commit()

        resp = make_response(jsonify(group_to.to_dict()))
        resp.status_code = HTTPStatus.OK

        return resp

    @staticmethod
    def delete_group(request, group_name):
        users_jwt = get_JWT_from_cookie()
        if not users_jwt:
            return error_message('Unauthorized!', status=HTTPStatus.UNAUTHORIZED)

        if not users_jwt['is_admin']:
            return error_message('Forbidden', status=HTTPStatus.FORBIDDEN)

        group = Group.query.filter_by(licence_id=users_jwt['licence_id'], name=group_name).first()
        if not group:
            return error_message(f'Group {group_name} does not exist!', HTTPStatus.NOT_FOUND)

        db.session.delete(group)
        db.session.commit()

        resp = make_response()
        resp.status_code = HTTPStatus.NO_CONTENT
        return resp
