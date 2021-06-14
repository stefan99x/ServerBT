from bson import json_util


class StatusService:
    def get_status_ON(self, mongo):
        status = mongo.db.TenantStatus.find({"statusName": "ON"})
        result = json_util.dumps(status)
        return result

    def get_status_INJURED(self, mongo):
        status = mongo.db.TenantStatus.find({"statusName": "INJURED"})
        result = json_util.dumps(status)
        return result

    def get_status_UNKNOWN(self, mongo):
        status = mongo.db.TenantStatus.find({"statusName": "UNKNOWN"})
        result = json_util.dumps(status)
        return result

    def get_status_NOT_IN_THE_BUILDING(self, mongo):
        status = mongo.db.TenantStatus.find({"statusName": "NOT IN THE BUILDING"})
        result = json_util.dumps(status)
        return result

    def get_status_tenant(self, mongo, id):
        status = mongo.db.TenantStatus.find({"tenantId": id})
        result = json_util.dumps(status)
        return result
