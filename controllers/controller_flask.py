from services.ApartmentsService import ApartmentsService
from flask import Flask, json, jsonify, request
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

        mongo.db.Tenants.insert(
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


@app.route("/tenants", methods=["GET"])
def get_tenats():
    tenants = mongo.db.Tenants.find()
    result = dumps(tenants)
    return result


@app.route("/tenants/<id>", methods=["GET"])
def get_tenant(id):
    tenant = mongo.db.Tenants.find({"_id": ObjectId(id)})
    result = dumps(tenant)
    return result


@app.route("/tenants/<id>", methods=["DELETE"])
def delete_tenant(id):
    mongo.db.Tenants.delete_one({"id": ObjectId(id)})
    response = jsonify("Tenant deleted successfully")
    response.status_code = 200
    return response


@app.route("/tenants/<id>", methods=["PUT"])
def update_tenant(id):
    _id = id
    _json = request.json
    _firstName = _json["firstName"]
    _lastName = _json["lastName"]
    _email = _json["email"]
    _password = _json["password"]
    _age = _json["age"]

    if (
        _firstName
        and _lastName
        and _email
        and _password
        and _age
        and request.method == "PUT"
    ):
        _hashed_password = generate_password_hash(_password)

        mongo.db.Tenants.update_one(
            {"_id": ObjectId(_id["$oid"]) if "$oid" in _id else ObjectId(_id)},
            {
                "$set": {
                    "firstName": _firstName,
                    "lastName": _lastName,
                    "email": _email,
                    "password": _hashed_password,
                    "age": _age,
                }
            },
        )

        response = jsonify("Update successfully")
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


@app.route("/injuries", methods=["POST"])
def add_injury():
    _json = request.json
    _bodyPartId = _json["bodyPartId"]
    _tenantId = _json["tenantId"]
    _description = _json["description"]

    if _bodyPartId and _tenantId and request.method == "POST":
        mongo.db.Injuries.insert(
            {
                "bodyPartId": _bodyPartId,
                "tenantId": _tenantId,
                "description": _description,
            }
        )

        response = jsonify("Injury Added Created")
        response.status_code = 200
        return response
    else:
        return not_found()


@app.route("/injuries", methods=["GET"])
def get_injuries():
    injuries = mongo.db.Injuries.find()
    result = dumps(injuries)
    return result


@app.route("/injuries/tenant/<id>", methods=["GET"])
def get_tenant_injuries(id):
    injuries = mongo.db.Injuries.find({"tenantId": ObjectId(id)})
    result = dumps(injuries)
    return result


@app.route("/injuries/<id>", methods=["DELETE"])
def delete_injury(id):
    mongo.db.Injuries.delete_one({"id": ObjectId(id)})
    response = jsonify("Injury deleted successfully")
    response.status_code = 200
    return response


@app.route("/injuries/<id>", methods=["PUT"])
def update_injury(id):
    _id = id
    _json = request.json
    _bodyPartId = _json["bodyPartId"]
    _tenantId = _json["tenantId"]
    _description = _json["description"]

    if _bodyPartId and _tenantId and request.method == "PUT":

        mongo.db.Injuries.update_one(
            {"_id": ObjectId(_id["$oid"]) if "$oid" in _id else ObjectId(_id)},
            {
                "$set": {
                    "bodyPartId": _bodyPartId,
                    "tenantId": _tenantId,
                    "description": _description,
                }
            },
        )

        response = jsonify("Update successfully")
        response.status_code = 200
        return response

    else:
        return not_found()



@app.route("/apartments", methods=["POST"])
def add_apartment():
    service = ApartmentsService()
    service.add_apartment(request,mongo)
    # _json = request.json
    # _floor = _json["floor"]
    # _number = _json["number"]
    # _tenantId = _json["tenantId"]

    # if _floor and _number and _tenantId and request.method == "POST":
    #     mongo.db.Apartments.insert(
    #         {
    #             "floor": _floor,
    #             "tenantId": _tenantId,
    #             "number": _number,
    #         }
    #     )

    #     response = jsonify("Apartment Added Created")
    #     response.status_code = 200
    #     return response
    # else:
    #     return not_found()


@app.route("/apartments", methods=["GET"])
def get_apartments():
    apartments = mongo.db.Apartments.find()
    result = dumps(apartments)
    return result


@app.route("/apartments/tenant/<id>", methods=["GET"])
def get_tenant(id):
    apartment = mongo.db.Apartments.find({"tenantId": ObjectId(id)})
    result = dumps(apartment)
    return result


if __name__ == "__main__":
    app.run(debug=True)