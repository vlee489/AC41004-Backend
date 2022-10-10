"""
Database module

This file contains shared & core DB functions.
"""
import motor.motor_asyncio
import app.database.models as DBModels
import certifi

ca = certifi.where()  # Used to deal with TLS certs not loading correctly on certain platforms


class DBConnector:
    def __init__(self, mongo_uri: str, db_name: str):
        """
        Constructor
        :param mongo_uri: MongoDB Connection URI
        :param db_name: DB Name
        """
        self._mongo_uri = mongo_uri
        self._db_name = db_name
        self._mongo_client: motor.motor_asyncio.AsyncIOMotorClient = None
        self._db: motor.motor_asyncio.AsyncIOMotorDatabase = None

    async def connect_db(self):
        """Create database connection."""
        self._mongo_client = motor.motor_asyncio.AsyncIOMotorClient(self._mongo_uri, tlsCAFile=ca)
        self._db = self._mongo_client[self._db_name]

    async def close_mongo_connection(self):
        """Close database connection."""
        self._mongo_client.close()

    from app.database.__user import get_user_via_email
    from app.database.__role import get_role_by_id
    from app.database.__customer import get_customer_by_id
    from app.database.__rule import get_rule_by_id, get_all_rules, get_rules_by_resource_type_id, \
        rules_by_resource_type_pipeline, get_all_rules_pipeline
    from app.database.__account import get_account_by_customer_id, get_account_by_id
    from app.database.__platform import get_platform_by_id
    from app.database.__resources import get_resource_by_id, get_resources_by_account_id, \
        get_non_compliant_resources_by_account_id, get_overview_count_by_account_id, \
        get_resource_by_account_id_and_not_in_id_list
    from app.database.__resourceType import get_resource_type_by_id
    from app.database.__nonCompliance import get_non_complaince_by_resource_id, get_non_complaince_by_rule_id
    from app.database.__nonComplianceAudit import get_non_compliance_audit_by_id, \
        get_non_compliance_audit_by_resource_id
    from app.database.__exceptionAudit import get_exception_audit_by_exception_id, add_exception_audit, \
        update_exception_audit
    from app.database.__exceptions import get_exception_from_exception_value, get_exception_by_date_account_id, \
        add_exception, update_exception, get_exception_from_exception_id
    from app.database.__search import search_account_id_resources
