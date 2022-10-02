"""
Security Coordinator

Handles all security management & authentication
"""
import aioredis
import uuid
import msgpack
import bcrypt
from fastapi import Request
import datetime
from typing import Optional

from app.database import DBConnector

from .models import UserSession, SessionSecurityProfile


class SecurityCoordinator:
    """API Security Coordinator"""

    def __init__(self, redis_uri: str, database: DBConnector):
        self.__redis_uri = redis_uri
        self.__redis_client: Optional[aioredis.client] = None
        self.__database = database

    async def start_up(self):
        """Start up functions."""
        self.__redis_client = await aioredis.from_url(self.__redis_uri)

    async def _cache_set_key(self, key: str, value: dict) -> bool:
        """
        Add Key:Value to Redis cache
        :param key: Key name
        :param value: Value Data dict
        :return: if operation was successful
        """
        _value = msgpack.packb(value, use_bin_type=True)
        async with self.__redis_client.client() as conn:
            return await conn.execute_command("SET", f"{key}", _value, "EX", "10800")

    async def _cache_get_key(self, key: str) -> Optional[dict]:
        """
        Retrieve value via key from Redis cache
        :param key: Key to retrieve data from
        :return: None or dict
        """
        if value := await self.__redis_client.get(f"{key}"):
            return msgpack.unpackb(value, raw=False)

    async def _cache_delete_key(self, key: str) -> None:
        """
        delete value via key from Redis cache
        :param key: Key to delete
        :return: None
        """
        await self.__redis_client.delete(f"{key}")

    async def create_session(self, request: Request, email: str, password: str) -> bool:
        """
        Completes Authorization Code Grant Request and creates session
        :param request: User's request
        :param email: User's email address
        :param password: User's password
        :return: if successful
        """
        await self.delete_session(request)  # delete existing sessions for user
        if not (user := await self.__database.get_user_via_email(email)):
            return False
        # Check if password is valid
        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return False
        if not (role := await user.get_role()):
            return False
        # If user gets past checks
        session_id = uuid.uuid4().hex
        expiry_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=10800)
        session_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "company": user.customer_id,
            "role_id": role.id,

            "session_expiry": expiry_date.isoformat(),
        }
        if await self._cache_set_key(session_id, session_data):
            request.session['security'] = {"session": session_id}
            return True

    async def delete_session(self, request: Request):
        """
        Delete a user's session (aka logout)
        :param request: User's request
        :return: None
        """
        if session_security := request.session.get("security"):
            if session_id := session_security.get("session", ""):
                await self._cache_delete_key(session_id)
                request.session.pop("security", {})
                return True
        return False

    async def get_security_profile(self, request: Request) -> Optional[SessionSecurityProfile]:
        """
        Get user's security session from profile
        :param request: User's request
        :return: Security profile or None
        """
        if session_central := request.session.get("security"):
            if session_data := await self._cache_get_key(session_central.get("session", "")):
                user_session = UserSession(session_data)
                return SessionSecurityProfile(session=user_session, database=self.__database)

