import json
from os import error
from bson import objectid
from passlib.hash import pbkdf2_sha256
from bson import json_util

from bson.objectid import ObjectId
from flask.json import jsonify


class TenantsService:
    def add_tenant(self, request, mongo):
        _json = json.loads(request.data)
        _email = _json["email"]
        _firstName = _json["firstName"]
        _lastName = _json["lastName"]
        _age = _json["age"]
        _password = _json["password"]

        if _email and _password and request.method == "POST":
            _hashed_password = pbkdf2_sha256.encrypt(_password)

            tenantId = mongo.db.Tenants.insert_one(
                {
                    "firstName": _firstName,
                    "lastName": _lastName,
                    "email": _email,
                    "password": _hashed_password,
                    "age": _age,
                }
            )

            mongo.db.TeantsStatus.insert_one(
                {
                    "tenantId": tenantId.inserted_id,
                    "tenantName": _firstName + _lastName,
                    "statusId": "60dac20652b08a49ac3be440",
                    "statusName": "UNKNOWN",
                }
            )

            mongo.db.Apartments.insert_one(
                {
                    "tenantId": tenantId.inserted_id,
                    "floor": 0,
                    "number": 0,
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
        _json = json.loads(request.data)
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
            _hashed_password = pbkdf2_sha256.hash(_password)

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
