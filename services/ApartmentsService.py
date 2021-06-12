from json import dumps
from bson.objectid import ObjectId
from bson import json_util
from flask.json import jsonify


class ApartmentsService:
    def add_apartment(self, request, mongo):
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

            resp = jsonify("Apartment Added Created")
            resp.status_code = 200
            return resp
        else:
            return 400

    def get_apartments(self, mongo):
        cursor = mongo.db.Apartments.find()
        list_cur = list(cursor)
        if not list_cur:
            return "No apartments"
        else:
            result = json_util.dumps(list_cur)
            return result

    def get_tenant_apartment(self, id, mongo):
        apartment = mongo.db.Apartments.find({"tenantId": id})
        result = json_util.dumps(apartment)
        return result
