from bson import json_util
from JWTUtils import JWTUtils
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256

from services.InjuriesService import InjuryService
from services.ApartmentsService import ApartmentsService
from services.TenantsService import TenantsService

app = Flask(__name__)
app.secret_key = "shh ii un secret"
app.config["MONGO_URI"] = "mongodb://localhost:27017/emergencyDatabase"

mongo = PyMongo(app)
tenantsService = TenantsService()
apartmentsService = ApartmentsService()
injuriesService = InjuryService()
jwtUtils = JWTUtils()


@app.route("/login", methods=["GET"])
def login():
    _json = request.json
    _email = _json["email"]
    _password = _json["password"]

    user = mongo.db.Tenants.find({"email": _email})
    user = list(eval(json_util.dumps(user)))
    userPassword = user[0]["password"]

    if pbkdf2_sha256.verify(_password, userPassword):
        return {
            "Token": JWTUtils.encode_token(
                jwtUtils, user[0]["_id"]["$oid"], user[0]["email"]
            )
        }, 200
    return {"Error": "No User with This credentials"}, 501


@app.route("/tenants", methods=["POST"])
def add_tenant():
    return tenantsService.add_tenant(request, mongo)


@app.route("/tenants", methods=["GET"])
def get_tenats():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return tenantsService.get_tenants(mongo)


@app.route("/tenants/<id>", methods=["GET"])
def get_tenant(id):
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return tenantsService.get_tenant(mongo, id)


@app.route("/tenants/<id>", methods=["DELETE"])
def delete_tenant(id):
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return tenantsService.delete_tenant(mongo, id)


@app.route("/tenants/<id>", methods=["PUT"])
def update_tenant(id):
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return tenantsService.update_tenant(mongo, request, id)


@app.errorhandler(404)
def not_found(error=None):
    message = {"status": 404, "message": "Not Found" + request.url}
    response = jsonify(message)
    response.status_code = 404
    return response


@app.route("/injuries", methods=["POST"])
def add_injury():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return injuriesService.add_injury(request, mongo)


@app.route("/injuries", methods=["GET"])
def get_injuries():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return injuriesService.get_injuries(mongo)


@app.route("/injuries/tenant/<id>", methods=["GET"])
def get_tenant_injuries(id):
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return injuriesService.get_tenant_injuries(mongo, id)


@app.route("/injuries/<id>", methods=["DELETE"])
def delete_injury(id):
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return injuriesService.delete_injury(mongo, id)


@app.route("/injuries/<id>", methods=["PUT"])
def update_injury(id):
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return injuriesService.update_injury(request, mongo, id)


@app.route("/apartments", methods=["POST"])
def add_apartment():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return apartmentsService.add_apartment(request, mongo)


@app.route("/apartments", methods=["GET"])
def get_apartments():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return apartmentsService.get_apartments(mongo)


@app.route("/apartments/tenant/<id>", methods=["GET"])
def get_tenant_apartment(id):
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return apartmentsService.get_tenant_apartment(id, mongo)


if __name__ == "__main__":
    app.run(debug=True)
