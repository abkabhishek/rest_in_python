
from flask import Flask, request, jsonify
from __main__ import db, ma, app, token_required

# Resource TEST


# Resource Test class/model
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(500))
    module_name = db.Column(db.String(50))

    def __init__(self, title, description, module_name):
        self.title = title
        self.description = description
        self.module_name = module_name


# Test Schema
class TestSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')


# init Test Schema
test_schema = TestSchema()
tests_schema = TestSchema(many=True)


@app.route("/test", methods=["POST"])
def add_test():
    title = request.json['title']
    description = request.json['description']
    module_name = request.json['module_name']

    new_test = Test(title, description, module_name)

    db.session.add(new_test)
    db.session.commit()

    return test_schema.jsonify(new_test), 201


@app.route("/test/<int:id>", methods=["PUT"])
def update_test(id):
    test = Test.query.get(id)
    title = request.json['title']
    description = request.json['description']
    module_name = request.json['module_name']

    test.title = title
    test.description = description
    test.module_name = module_name

    db.session.commit()

    return test_schema.jsonify(test), 201


@app.route("/tests", methods=["GET"])
@token_required
def get_all_tests():
    all_tests = Test.query.all()
    results = tests_schema.dump(all_tests)
    return jsonify(results)


@app.route("/test/<int:id>", methods=["GET"])
def get_single_tests(id):
    test = Test.query.get(id)
    return test_schema.jsonify(test)