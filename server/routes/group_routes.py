from flask import request

from server import app
from server.config import URI_PREFIX
from server.groups import GroupAPI


@app.route(URI_PREFIX+'/permissions/add', methods=['POST'])
def add_permission_group():
    response = GroupAPI.add_group(request)
    return response


@app.route(URI_PREFIX+'/permissions', methods=['GET'])
def get_permission_groups():
    response = GroupAPI.get_all_groups(request)
    return response


@app.route(URI_PREFIX+'/permissions/<group_name>', methods=['PUT', 'DELETE'])
def set_delete_permission_group(group_name):
    response = None
    
    if request.method == 'PUT':
        response = GroupAPI.set_group(request, group_name)
    else:
        response = GroupAPI.delete_group(request, group_name)
    
    return response
