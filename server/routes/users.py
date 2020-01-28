from flask import jsonify, request, make_response
from http import HTTPStatus

from server import app, db
from server.utils import encode_JWT, decode_JWT, get_JWT_from_cookie, error_message, hash_password
from server.config import JWT_COOKIE_NAME
from server.models.schemas import LoginUserSchema, CreateUserSchema
from server.models.models import User


login_user_schema = LoginUserSchema()
create_user_schema = CreateUserSchema()
URI_PREFIX = '/api/v1/users'

# ======== USERS ========

@app.route(URI_PREFIX+'/login', methods=['POST'])
def login():
    # result = {
    #     'endpoint': URI_PREFIX+'/login',
    #     'method': request.method,
    #     'parameter': None
    # }

    errors = login_user_schema.validate(request.json)
    if errors:
        return error_message(str(errors), HTTPStatus.BAD_REQUEST)

    pass_hash = hash_password(request.json['password'])
    user = User.query.filter_by(username=request.json['username'], password_hash=pass_hash).first()
    if user is None:
        return error_message('Wrong username or password!', HTTPStatus.BAD_REQUEST)

    encoded = encode_JWT(user.to_jwt_dict())

    resp = make_response(jsonify(user.to_jwt_dict()))
    resp.set_cookie(JWT_COOKIE_NAME, encoded)
    return resp

@app.route(URI_PREFIX+'/token/refresh', methods=['GET'])
def refresh_token():
    users_jwt = get_JWT_from_cookie()
    if 'exp' in users_jwt:
        users_jwt.pop('exp')
    encoded = encode_JWT(users_jwt)
    resp = make_response(jsonify({'token': encoded}))
    resp.set_cookie(JWT_COOKIE_NAME, encoded)
    return resp

@app.route(URI_PREFIX+'/register', methods=['POST'])
def register():
    # result = {
    #     'endpoint': URI_PREFIX+'/register',
    #     'method': request.method,
    #     'parameter': None
    # }
    # decoded_jwt = get_JWT_from_cookie()
    # if not decoded_jwt:
    #     return error_message('Wrong JWT!', HTTPStatus.UNAUTHORIZED)
    # return jsonify(result)
    errors = create_user_schema.validate(request.json)
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
        
    return jsonify(new_user.to_jwt_dict()), HTTPStatus.CREATED

@app.route(URI_PREFIX, methods=['GET'])
def users_list():
    result = {
        'endpoint': URI_PREFIX,
        'method': request.method,
        'parameter': None
    }
    return jsonify(result)

@app.route(URI_PREFIX+'/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_details(user_id):
    result = {
        'endpoint': URI_PREFIX+'/<int:user_id>',
        'method': request.method,
        'parameter': user_id
    }
    return jsonify(result)
    # if request.method == 'GET': # GET
        
    # elif request.method == 'PUT': # PUT
        
    # else: # DELETE

    # pass

@app.route(URI_PREFIX+'/<int:user_id>/avatar', methods=['PUT'])
def set_user_avatar(user_id):
    result = {
        'endpoint': URI_PREFIX+'/<int:user_id>/avatar',
        'method': request.method,
        'parameter': user_id
    }
    return jsonify(result)

@app.route(URI_PREFIX+'/<int:user_id>/permissions', methods=['PUT'])
def set_user_groups(user_id):
    result = {
        'endpoint': URI_PREFIX+'/<int:user_id>/permissions',
        'method': request.method,
        'parameter': user_id
    }
    return jsonify(result)

# ======== PERMISSION GROUPS ========

@app.route(URI_PREFIX+'/permissions/add', methods=['POST'])
def add_permission_group():
    result = {
        'endpoint': URI_PREFIX+'/permissions/add',
        'method': request.method,
        'parameter': None
    }
    return jsonify(result)

@app.route(URI_PREFIX+'/permissions', methods=['GET'])
def get_permission_groups():
    result = {
        'endpoint': URI_PREFIX+'/permissions',
        'method': request.method,
        'parameter': None
    }
    return jsonify(result)

@app.route(URI_PREFIX+'/permissions/<group_name>', methods=['PUT', 'DELETE'])
def set_delete_permission_group(group_name):
    result = {
        'endpoint': URI_PREFIX+'/permissions/<group_name>',
        'method': request.method,
        'parameter': group_name
    }
    return jsonify(result)