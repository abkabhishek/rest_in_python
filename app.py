import os
import datetime
from functools import wraps

import jwt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init App
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SECRET_KEY'] = "ThisIsMySecretKeyForSure"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

def token_required(f):

    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {'message':"token not found"}, 401

        print("Token : {}".format(token))
        return f(*args, **kwargs)

    return decorated

import Tests
import Users

@app.route("/login")
def login():
    auth = request.authorization
    if auth and auth.username == 'abk':
        payload = {
            'user_id': "abk",
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        }
        jwt_token = jwt.encode(payload, app.config['SECRET_KEY'])
        return jsonify({'token': jwt_token.decode('utf-8')})
    else:
        return jsonify({"message": "Not Logged in"})


@app.route("/", methods=['GET'])
def Home():
    return jsonify({"message": "Home Page"})


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
