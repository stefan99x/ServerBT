from json import dumps
from bson.objectid import ObjectId
from flask.json import jsonify


class ApartmentsService:
    def add_apartment(self, request, mongo):
        _json = request.json
        _floor = _json['floor']
        _number = _json['number']
        _tenantId = _json['tenantId']

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
        apartments = mongo.db.Apartments.find()
        if(apartments.retrieved == 0):
            return "No apartments"
        else:
            result = dumps(apartments)
            return result

    def get_tenant_apartment(self, id, mongo):
        apartment = mongo.db.Apartments.find({"tenantId": ObjectId(id)})
        result = dumps(apartment)
        return result
