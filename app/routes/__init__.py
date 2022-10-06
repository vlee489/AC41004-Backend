"""FastAPI Routes"""
from .exceptions import router as exception_router
from .session import router as session_router
from .user import router as user_router
from .account import router as account_router
from .ruleOverview import router as rule_overview_router
from .resources import router as resource_router
from .rule import router as rule_router
from .compliance import router as compliance_router
from .ruleExceptions import router as exception_router
from .accountOverview import router as account_overview_router