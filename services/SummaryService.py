from flask.json import jsonify


class SummaryService:
    def get_summary(self, mongo):
        numberOfInjuriesCount = mongo.db.Injuries.find().count()
        totalTenantsCount = mongo.db.Tenants.find().count()
        onlineTenantsCount = (
            mongo.db.TenantStatus.find({"statusName": "ON"}).count()
            + mongo.db.TenantStatus.find({"statusName": "INJURED"}).count()
        )
        statusUNKNOWNCount = mongo.db.TenantStatus.find(
            {"statusName": "UNKNOWN"}
        ).count()
        return jsonify(
            totalTenants=totalTenantsCount,
            numberOfInjuries=numberOfInjuriesCount,
            onlineTenants=onlineTenantsCount,
            statusUnknown=statusUNKNOWNCount,
        )
