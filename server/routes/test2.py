from flask import jsonify
from server import app

@app.route('/test2/')
def t2():
    return jsonify({'message': 'test message 2'})
