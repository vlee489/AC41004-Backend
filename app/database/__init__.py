"""
Database module

This file contains shared & core DB functions.
"""
import motor.motor_asyncio
import app.database.models as DBModels
import certifi
ca = certifi.where()


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

