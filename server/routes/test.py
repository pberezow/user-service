from flask import jsonify
from server import app

@app.route('/')
def hello():
    return 'Hello!'

@app.route('/test')
def test():
    return jsonify({'message': 'test message'})