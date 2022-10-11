"""Customer Account DB Model"""
from dataclasses import dataclass, field
from bson import objectid

from .base import Base


@dataclass
class Account(Base):
    reference: str = field(init=False, default="")
    platform_id: str = field(init=False, default="")
    customer_id: str = field(init=False, default="")

    def __post_init__(self, init_data: dict):
        super().__post_init__(init_data)
        self.reference = init_data.get("reference", "")

        self._platform_id = init_data.get("platform_id", "")
        self.platform_id = str(self._platform_id)

        self._customer_id = init_data.get("customer_id", "")
        self.customer_id = str(self._customer_id)

    @property
    def platform_object_id(self) -> objectid.ObjectId:
        """
        Get platform's objectID
        :return:
        """
        return self._platform_id

    @property
    def customer_object_id(self) -> objectid.ObjectId:
        """
        Get customer's objectID
        :return:
        """
        return self._customer_id

    def api_response(self, customer: dict, platform: dict) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "reference": self.reference,
            "platform": platform,
            "customer": customer
        }
