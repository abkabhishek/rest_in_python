
from flask import Flask, request, jsonify
from __main__ import db, ma, app, token_required


# Resource User class/model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    status = db.Column(db.String(30))
    type = db.Column(db.String(30))

    def __init__(self, username, password, type):
        self.username = username
        self.password = password
        self.status = "active"
        self.type = type


# Test Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'status', 'type')


# init Test Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    password = request.json['password']
    type = request.json['type']

    new_user = User(username, password, type)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201


@app.route("/users", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    results = users_schema.dump(all_users)
    return jsonify(results)