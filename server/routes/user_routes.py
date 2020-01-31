from flask import request, jsonify  # drop jsonify later

from server import app
from server.config import URI_PREFIX
from server.users import UserAPI


@app.route(URI_PREFIX+'/login', methods=['POST'])
def login():
    response = UserAPI.login(request)
    return response


@app.route(URI_PREFIX+'/logout', methods=['GET'])
def logout():
    response = UserAPI.logout(request)
    return response


@app.route(URI_PREFIX+'/token/refresh', methods=['GET'])
def refresh_token():
    response = UserAPI.refresh_token(request)
    return response


@app.route(URI_PREFIX+'/register', methods=['POST'])
def register():
    response = UserAPI.register(request)
    return response


@app.route(URI_PREFIX, methods=['GET'])
def users_list():
    response = UserAPI.users_list(request)
    return response


@app.route(URI_PREFIX+'/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_details(user_id):
    response = None
    if request.method == 'GET':
        response = UserAPI.user_details_GET(request, user_id)
    elif request.method == 'PUT':
        response = UserAPI.user_details_PUT(request, user_id)
    else:
        response = UserAPI.user_details_DELETE(request, user_id)
    return response


@app.route(URI_PREFIX+'/<int:user_id>/password', methods=['PUT'])
def set_user_password(user_id):
    response = UserAPI.set_user_password(request, user_id)
    return response


@app.route(URI_PREFIX+'/<int:user_id>/avatar', methods=['PUT'])
def set_user_avatar(user_id):
    response = UserAPI.set_user_avatar(request, user_id)
    return response


@app.route(URI_PREFIX+'/<int:user_id>/permissions', methods=['PUT'])
def set_user_groups(user_id):
    response = UserAPI.set_user_groups(request, user_id)
    return response
