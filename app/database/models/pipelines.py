"""Handles responses for MongoDB Pipelines that aggregate data"""
from dataclasses import dataclass, field, InitVar
from typing import Optional

from .rule import Rule
from .resourceType import ResourceType
from .platform import Platform


@dataclass
class RuleResourceTypePipeline:
    init_data: InitVar[dict]
    rule: Optional[Rule] = field(init=False, default=None)
    resource_type: Optional[ResourceType] = field(init=False, default=None)
    platform: Optional[Platform] = field(init=False, default=None)

    def __post_init__(self, init_data: dict):
        self.rule = Rule(init_data)
        if "resource_type" in init_data:
            self.resource_type = ResourceType(init_data["resource_type"])
            if "platform" in init_data['resource_type']:
                self.platform = Platform(init_data['resource_type']["platform"])

