from http import HTTPStatus
from flask import make_response, jsonify

from server import db
from server.groups.abstract_group_api import AbstractGroupAPI
from server.utils import error_message, get_JWT_from_cookie
from server.models.entity import Group
from server.models.validators import create_group_validator
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

        form = request.json
        form['licence_id'] = users_jwt['licence_id']
        errors = create_group_validator.validate(form)
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
        return error_message('Not implemented yet!', status=HTTPStatus.NOT_FOUND)

    @staticmethod
    def delete_group(request, group_name):
        return error_message('Not implemented yet!', status=HTTPStatus.NOT_FOUND)
