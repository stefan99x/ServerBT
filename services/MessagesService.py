import json
from bson import json_util
from flask.json import jsonify


class MessagesService:
    def get_messages(self, mongo):
        status = mongo.db.Messages.find()
        result = json_util.dumps(status)
        return result

    def post_message(self, request, mongo):
        _json = json.loads(request.data)
        _message = _json["message"]
        _tenantName = _json["tenantName"]

        mongo.db.Messages.insert(
            {
                "tenantName": _tenantName,
                "message": _message,
            }
        )

        response = jsonify("Message Posted")
        response.status_code = 200
        return response
