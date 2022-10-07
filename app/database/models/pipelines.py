"""Handles responses for MongoDB Pipelines that aggregate data"""
from dataclasses import dataclass, field, InitVar
from typing import Optional
import motor.motor_asyncio

from .rule import Rule
from .resourceType import ResourceType
from .platform import Platform
from .customer import Customer
from .user import User
from .exception import RuleException
from .resource import Resource
from .exceptionAudit import ExceptionAudit


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


@dataclass
class ExceptionPipeline:
    init_data: InitVar[dict]
    database: InitVar[motor.motor_asyncio.AsyncIOMotorDatabase]
    exception: Optional[RuleException] = field(init=False, default=None)
    customer: Optional[Customer] = field(init=False, default=None)
    user: Optional[User] = field(init=False, default=None)
    rule_resource_type: Optional[RuleResourceTypePipeline] = field(init=False, default=None)

    def __post_init__(self, init_data: dict, database: motor.motor_asyncio.AsyncIOMotorDatabase):
        self.exception = RuleException(init_data)
        if "customer" in init_data:
            self.customer = Customer(init_data['customer'])
        if 'last_updated_by_user' in init_data:
            self.user = User(init_data['last_updated_by_user'], database)
        if 'rule' in init_data:
            self.rule_resource_type = RuleResourceTypePipeline(init_data['rule'])


@dataclass
class AccountExceptionPipeline(ExceptionPipeline):
    resource: Optional[Resource] = field(init=False, default=None)

    def __post_init__(self, init_data: dict, database: motor.motor_asyncio.AsyncIOMotorDatabase):
        super().__post_init__(init_data, database)
        self.resource = Resource(init_data.get('resource', None))


@dataclass
class ExceptionAuditPipeline:
    init_data: InitVar[dict]
    database: InitVar[motor.motor_asyncio.AsyncIOMotorDatabase]
    exception_audit: Optional[ExceptionAudit] = field(init=False, default=None)
    exception: Optional[RuleException] = field(init=False, default=None)
    customer: Optional[Customer] = field(init=False, default=None)
    user: Optional[User] = field(init=False, default=None)
    rule_resource_type: Optional[RuleResourceTypePipeline] = field(init=False, default=None)

    def __post_init__(self, init_data: dict, database: motor.motor_asyncio.AsyncIOMotorDatabase):
        self.exception_audit = ExceptionAudit(init_data)
        if "exception" in init_data:
            self.exception = RuleException(init_data['customer'])
        if "customer" in init_data:
            self.customer = Customer(init_data['customer'])
        if 'user' in init_data:
            self.user = User(init_data['user'], database)
        if 'rule' in init_data:
            self.rule_resource_type = RuleResourceTypePipeline(init_data['rule'])

