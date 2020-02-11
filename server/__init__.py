from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from py_eureka_client import eureka_client

from server.config import SQLALCHEMY_DATABASE_URI, EUREKA_IP, DEFAULT_IP, DEFAULT_PORT

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from server.models.entity import *

from server.routes import *

eureka_client.init(
                   eureka_server=EUREKA_IP,
                   app_name='user_service',
                   instance_port=DEFAULT_PORT
)
