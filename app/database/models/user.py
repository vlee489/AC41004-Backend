"""User DB Model"""
from dataclasses import dataclass, InitVar, field
from typing import Optional
from bson import objectid
import motor.motor_asyncio

from .userRole import UserRole

@dataclass
class User:
    """User DB Model"""
    user_data: InitVar[dict]
    database: InitVar[motor.motor_asyncio.AsyncIOMotorDatabase]
    id: str = field(init=False, default="")

    email: str = field(init=False, default="")
    password_hash: str = field(init=False, default=b"")
    first_name: str = field(init=False, default="")
    last_name: str = field(init=False, default="")

    role_id: str = field(init=False, default="")
    customer_id: str = field(init=False, default="")

    def __post_init__(self, user_data: dict, database: motor.motor_asyncio.AsyncIOMotorDatabase):
        self._id = user_data.get("_id", "")
        self.id = str(self._id)

        self.__db = database

        self.email = user_data.get("email", "")
        self.password_hash = user_data.get("password_hash", b"")
        self.first_name = user_data.get("first_name", "")
        self.last_name = user_data.get("last_name", "")

        self._role_id = user_data.get("role_id", "")
        self.role_id = str(self._role_id)

        self._customer_id = user_data.get("customer_id", "")
        self.customer_id = str(self._customer_id)

    @property
    def object_id(self) -> objectid.ObjectId:
        """
        Get user's objectID
        :return:
        """
        return self._id

    @property
    def customer_object_id(self) -> objectid.ObjectId:
        """
        Return user's customer object ID
        :return:
        """
        return self._customer_id

    async def get_role(self) -> Optional[UserRole]:
        if role := await self.__db.userRoles.find_one({"_id": self._role_id}):
            return UserRole(role)
