from controllers.controller_flask import not_found
from json import dumps
from bson.objectid import ObjectId
from flask.json import jsonify


class ApartmentsService:
    def add_apartment(request, mongo):
        _json = request.json
        _floor = _json["floor"]
        _number = _json["number"]
        _tenantId = _json["tenantId"]

        if _floor and _number and _tenantId and request.method == "POST":
            mongo.db.Apartments.insert(
                {
                    "floor": _floor,
                    "tenantId": _tenantId,
                    "number": _number,
                }
            )

            response = jsonify("Apartment Added Created")
            response.status_code = 200
            return response
        else:
            return not_found()

    def get_apartments(mongo):
        apartments = mongo.db.Apartments.find()
        result = dumps(apartments)
        return result

    def get_tenant_apartment(id, mongo):
        apartment = mongo.db.Apartments.find({"tenantId": ObjectId(id)})
        result = dumps(apartment)
        return result
