from json import dumps
from bson import json_util

from bson.objectid import ObjectId
from flask.json import jsonify
from werkzeug.security import generate_password_hash, check_password_hash


class TenantsService:
    def add_tenant(self, request, mongo):
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
            return 400

    def get_tenants(self, mongo):
        tenants = mongo.db.Tenants.find()
        result = json_util.dumps(tenants)
        return result

    def get_tenant(self, mongo, id):
        tenant = mongo.db.Tenants.find({"_id": ObjectId(id)})
        result = json_util.dumps(tenant)
        return result

    def delete_tenant(self, mongo, id):
        mongo.db.Tenants.delete_one({"_id": ObjectId(id)})
        response = jsonify("Tenant deleted successfully")
        response.status_code = 200
        return response

    def update_tenant(self, mongo, request, id):
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
            return 400
