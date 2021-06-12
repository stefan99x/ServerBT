from bson import json_util


class StatusService:
    def get_status_ON(self, mongo):
        status = mongo.db.TenantStatus.find({"statusName":"ON (TRAPPED BUT SAFE)"})
        result = json_util.dumps(status)
        return result

    def get_status_INJURED(self, mongo):
        status = mongo.db.TenantStatus.find({"statusName":"INJURED"})
        result = json_util.dumps(status)
        return result

    def get_status_UNKNOWN(self, mongo):
        status = mongo.db.TenantStatus.find({"statusName":"UNKNOWN"})
        result = json_util.dumps(status)
        return result

    def get_status_NOT_IN_THE_BUILDING(self, mongo):
        status = mongo.db.TenantStatus.find({"statusName":"NOT IN THE BUILDING"})
        result = json_util.dumps(status)
        return result