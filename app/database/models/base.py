"""
Base DB Model

Acts as a class that most DB models will inherit from
"""
from dataclasses import dataclass, InitVar, field
from bson import objectid


@dataclass
class Base:
    init_data: InitVar[dict]
    id: str = field(init=False, default="")

    name: str = field(init=False, default="")

    def __post_init__(self, init_data: dict):
        self._id = init_data.get("_id", "")
        self.id = str(self._id)

        self.name = init_data.get("name", "")

    @property
    def object_id(self) -> objectid.ObjectId:
        """
        Get base's objectID
        :return:
        """
        return self._id
