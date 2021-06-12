from json import dumps
from bson import json_util
import json

from bson.objectid import ObjectId
from flask.json import jsonify


class InjuryService:
    def add_injury(self, request, mongo):
        _json = json.loads(request.data)
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
        result = json_util.dumps(injuries)
        return result

    def get_tenant_injuries(self, mongo, id):
        injuries = mongo.db.Injuries.find({"tenantId": id})
        result = json_util.dumps(injuries)
        return result

    def delete_injury(self, mongo, id):
        mongo.db.Injuries.delete_one({"_id": ObjectId(id)})
        response = jsonify("Injury deleted successfully")
        response.status_code = 200
        return response

    def update_injury(self, request, mongo, id):
        _json = json.loads(request.data)
        _id = _json["_id"]
        _bodyPartId = _json["bodyPartId"]
        _bodyPartName = _json["bodyPartName"]
        _tenantId = _json["tenantId"]
        _tenantName = _json["tenantName"]
        _description = _json["description"]
        print(request.json)
        if _bodyPartId and _tenantId and request.method == "PUT":

            mongo.db.Injuries.update_one(
                {"_id": ObjectId(_id["$oid"]) if "$oid" in _id else ObjectId(_id)},
                {
                    "$set": {
                        "bodyPartId": _bodyPartId,
                        "bodyPartName": _bodyPartName,
                        "tenantId": _tenantId,
                        "description": _description,
                        "tenantName": _tenantName,
                    }
                },
            )

            response = jsonify("Update successfully")
            response.status_code = 200
            return response

        else:
            return 400
