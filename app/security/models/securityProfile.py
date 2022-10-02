from typing import Optional, List
from app.database import DBConnector
from app.database.models import UserRole
from .session import UserSession


class SessionSecurityProfile:
    """Security profile for user's with a cookie session"""

    def __init__(self, **kwargs):
        self.session: UserSession = kwargs.get("session")
        self.__db: DBConnector = kwargs.get("database")

    async def __get_role(self) -> Optional[UserRole]:
        return await self.__db.get_role_by_id(self.session.role_id)

    async def check_permissions(self, **kwargs) -> bool:
        """
        Check if user has permission to resource & action
        :key required_level (int): Required level for resource
        :key customer_resource_id (str): customer ID of resource
        :return: if permission is granted to resource and action
        """
        required_level: int = kwargs.get("level")
        customer_resource_id: str = kwargs.get("customer_resource_id")
        if customer_resource_id == self.session.customer_id:
            role = await self.__get_role()
            if role and required_level:
                if role.level >= required_level:
                    return True
        return False
