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
        :key level (int): Required level for resource
        :key resource_customer_id (str): customer ID of resource
        :key resource_account_id (str): account ID of resource
        :return: if permission is granted to resource and action
        """
        required_level: int = kwargs.get("level")
        resource_customer_id: str = kwargs.get("resource_customer_id", None)
        resource_account_id: str = kwargs.get("resource_account_id", None)

        cont = False  # Continue
        if resource_customer_id and (resource_customer_id == self.session.customer_id):
            cont = True
        elif resource_account_id:
            if account := await self.__db.get_account_by_id(resource_account_id):
                if account.customer_id == self.session.customer_id:
                    cont = True
        if cont:
            role = await self.__get_role()
            if (role is not None) and (required_level is not None):
                if required_level <= role.level:
                    return True
        return False
