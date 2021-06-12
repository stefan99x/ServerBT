
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash

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


@app.route("/tenants", methods=["POST"])
def add_tenant():
    return tenantsService.add_tenant(request, mongo)


@app.route("/tenants", methods=["GET"])
def get_tenats():
    return tenantsService.get_tenants(mongo)


@app.route("/tenants/<id>", methods=["GET"])
def get_tenant(id):
    return tenantsService.get_tenant(mongo, id)


@app.route("/tenants/<id>", methods=["DELETE"])
def delete_tenant(id):
    return tenantsService.delete_tenant(mongo, id)


@app.route("/tenants/<id>", methods=["PUT"])
def update_tenant(id):
    return tenantsService.update_tenant(mongo, request, id)


@app.errorhandler(404)
def not_found(error=None):
    message = {"status": 404, "message": "Not Found" + request.url}
    response = jsonify(message)
    response.status_code = 404
    return response


@app.route("/injuries", methods=["POST"])
def add_injury():
    return injuriesService.add_injury(request, mongo)


@app.route("/injuries", methods=["GET"])
def get_injuries():
    return injuriesService.get_injuries(mongo)


@app.route("/injuries/tenant/<id>", methods=["GET"])
def get_tenant_injuries(id):
    return injuriesService.get_tenant_injuries(mongo, id)


@app.route("/injuries/<id>", methods=["DELETE"])
def delete_injury(id):
    return injuriesService.delete_injury(mongo, id)


@app.route("/injuries/<id>", methods=["PUT"])
def update_injury(id):
    return injuriesService.update_injury(request, mongo, id)


@app.route("/apartments", methods=["POST"])
def add_apartment():
    return apartmentsService.add_apartment(request, mongo)


@app.route("/apartments", methods=["GET"])
def get_apartments():
    return apartmentsService.get_apartments(mongo)


@app.route("/apartments/tenant/<id>", methods=["GET"])
def get_tenant_apartment(id):
    return apartmentsService.get_tenant_apartment(id, mongo)


if __name__ == "__main__":
    app.run(debug=True)
