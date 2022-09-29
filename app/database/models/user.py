"""User DB Model"""
from dataclasses import dataclass, InitVar, field
from bson import objectid


@dataclass
class User:
    """User DB Model"""
    user_data: InitVar[dict]
    id: str = field(init=False, default="")

    email: str = field(init=False, default="")
    password_hash: bytes = field(init=False, default=b"")
    first_name: str = field(init=False, default="")
    last_name: str = field(init=False, default="")

    role: int = field(init=False, default=0)
    customer_id: str = field(init=False, default="")

    def __post_init__(self, user_data: dict):
        self._id = user_data.get("_id", "")
        self.id = str(self._id)

        self.email = user_data.get("email", "")
        self.password_hash = user_data.get("password_hash", b"")
        self.first_name = user_data.get("first_name", "")
        self.last_name = user_data.get("last_name", "")

        self.role = user_data.get("role", 0)
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
