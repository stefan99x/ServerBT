from services.MessagesService import MessagesService
from services.StatusService import StatusService
from services.SummaryService import SummaryService
from bson import json_util
from JWTUtils import JWTUtils
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256


from services.InjuriesService import InjuryService
from services.ApartmentsService import ApartmentsService
from services.TenantsService import TenantsService

app = Flask(__name__)
CORS(app)
app.secret_key = "shh ii un secret"
app.config["MONGO_URI"] = "mongodb://localhost:27017/emergencyDatabase"


mongo = PyMongo(app)
tenantsService = TenantsService()
apartmentsService = ApartmentsService()
injuriesService = InjuryService()
summaryService = SummaryService()
statusService = StatusService()
messagesService = MessagesService()
jwtUtils = JWTUtils()


@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    _json = request.json
    _email = _json["email"]
    _password = _json["password"]

    user = mongo.db.Tenants.find({"email": _email})
    user = list(eval(json_util.dumps(user)))
    userPassword = user[0]["password"]

    if pbkdf2_sha256.verify(_password, userPassword):
        # mongo.db.TenantStatus.update_one(
        #     {
        #         {"tenantId": user[0]["_id"]["$oid"]},
        #         {
        #             "$set": {
        #                 "statusId": "60c8f7e84e823f11a3143447",
        #                 "statusName": "ON",
        #             }
        #         }
        #     },
        # )
        return {
            "token": JWTUtils.encode_token(
                jwtUtils, user[0]["_id"]["$oid"], user[0]["email"]
            ),
            "firstName": user[0]["firstName"],
            "lastName": user[0]["lastName"],
            "age": user[0]["age"],
            "email": user[0]["email"],
            "id": user[0]["_id"]["$oid"],
        }, 200
    return {"Error": "No User with This credentials"}, 501


@app.route("/register", methods=["POST"])
@cross_origin()
def add_tenant():
    return tenantsService.add_tenant(request, mongo)


@app.route("/tenants", methods=["GET"])
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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


@app.route("/apartments/tenant/<id>", methods=["PUT"])
@cross_origin()
def update_tenant_apartment(id):
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return apartmentsService.update_apartment(id, request, mongo)


@app.route("/summary", methods=["GET"])
@cross_origin()
def get_summary():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return summaryService.get_summary(mongo)


@app.route("/status/ON", methods=["GET"])
@cross_origin()
def get_status_ON():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return statusService.get_status_ON(mongo)


@app.route("/status/INJURED", methods=["GET"])
@cross_origin()
def get_status_INJURED():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return statusService.get_status_INJURED(mongo)


@app.route("/status/UNKNOWN", methods=["GET"])
@cross_origin()
def get_status_UNKNOWN():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return statusService.get_status_UNKNOWN(mongo)


@app.route("/status/NOT_IN_THE_BUILDING", methods=["GET"])
@cross_origin()
def get_status_NOT_IN_THE_BUILDING():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return statusService.get_status_NOT_IN_THE_BUILDING(mongo)


@app.route("/messages", methods=["GET"])
@cross_origin()
def get_messages():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return messagesService.get_messages(mongo)


@app.route("/messages", methods=["POST"])
@cross_origin()
def post_message():
    try:
        token = request.headers.get("Authorization").split(" ")[-1]
    except Exception as ex:
        return {"error": "Please login"}, 401
    try:
        user = JWTUtils.decode_token(jwtUtils, token)
    except Exception as ex:
        return {"error": str(ex)}, 401
    return messagesService.post_message(request, mongo)


if __name__ == "__main__":
    app.run(debug=True)
