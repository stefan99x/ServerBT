from json import dumps

from bson.objectid import ObjectId
from flask.json import jsonify


class InjuryService:
    def add_injury(self, request, mongo):
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
            return 400

    def get_injuries(self, mongo):
        injuries = mongo.db.Injuries.find()
        result = dumps(injuries)
        return result

    def get_tenant_injuries(self, mongo, id):
        injuries = mongo.db.Injuries.find({"tenantId": ObjectId(id)})
        result = dumps(injuries)
        return result

    def delete_injury(self, mongo, id):
        mongo.db.Injuries.delete_one({"id": ObjectId(id)})
        response = jsonify("Injury deleted successfully")
        response.status_code = 200
        return response

    def update_injury(self, request, mongo, id):
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
            return 400
