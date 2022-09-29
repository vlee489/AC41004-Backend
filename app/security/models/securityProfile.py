from typing import Optional, List
from app.database import DBConnector
from .session import UserSession


class SessionSecurityProfile:
    """Security profile for user's with a cookie session"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session: UserSession = kwargs.get("session")
        self.__db: DBConnector = kwargs.get("database")

    async def check_permissions(self, **kwargs):
        # TODO implement role checks
        pass
