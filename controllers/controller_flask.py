from dns import message
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers import response

app = Flask(__name__)
app.secret_key = "shh ii un secret"
app.config["MONGO_URI"] = "mongodb://localhost:27017/emergencyDatabase"

mongo = PyMongo(app)


@app.route("/tenants", methods=["POST"])
def add_user():
    _json = request.json
    _email = _json["email"]
    _firstName = _json["firstName"]
    _lastName = _json["lastName"]
    _age = _json["age"]
    _password = _json["password"]

    if _email and _password and request.method == "POST":
        _hashed_password = generate_password_hash(password=_password)

        id = mongo.db.Tenants.insert(
            {
                "firstName": _firstName,
                "lastName": _lastName,
                "email": _email,
                "password": _hashed_password,
                "age": _age,
            }
        )

        response = jsonify("Account Created")
        response.status_code = 200
        return response
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {"status": 404, "message": "Not Found" + request.url}
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
