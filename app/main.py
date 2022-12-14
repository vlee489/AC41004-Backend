from fastapi import Request, FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import logging
import uvicorn

from app.database import DBConnector
from app.security import SecurityCoordinator
from app.functions import Config

from app.routes import *

system_variables = Config()  # load in config file

debug = system_variables.debug

origins = [
    "http://localhost",
    "file:///",
    "http://localhost:63342",
    "http://127.0.0.1:5500",
    "https://ac41004.vlee.me.uk",
    "https://ac41004-frontend.pages.dev",
    "https://ac41004-frontend.pages.dev"
]

# Initialize logging
logging.basicConfig(
    level=(
        logging.DEBUG if debug else logging.INFO
    ),
    format='\033[31m%(levelname)s\033[0m \033[90min\033[0m \033[33m%(filename)s\033[0m \033[90mon\033[0m %(asctime)s\033[90m:\033[0m %(message)s',
    datefmt='\033[32m%m/%d/%Y\033[0m \033[90mat\033[0m \033[32m%H:%M:%S\033[0m'
)
logging.getLogger("fastapi").setLevel(logging.ERROR)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("motor").setLevel(logging.ERROR)
logging.getLogger(__name__)
if debug:
    logging.info("static.env - 'DEBUG' key found. Running in debug mode, do not use in production.")


def create_app():
    new_app = FastAPI(
        title="ITP API",
        description="ITP API Service",
        docs_url="/internaldocs",
        redoc_url="/docs"
    )
    # Set up DB & API connections
    new_app.db = DBConnector(system_variables.mongo_uri, system_variables.db_name)
    new_app.security = SecurityCoordinator(system_variables.redis_uri, new_app.db)

    # Startup and Shutdown Events
    @new_app.on_event("startup")
    async def startup():
        await new_app.db.connect_db()
        await new_app.security.start_up()

    @new_app.on_event("shutdown")
    async def shutdown():
        await new_app.db.close_mongo_connection()

    # Add cors
    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        # allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add session middleware
    new_app.add_middleware(SessionMiddleware, secret_key=system_variables.session_secret, max_age=10800,
                           same_site="none", https_only=True)

    # Routes
    new_app.include_router(
        session_router,
        prefix="/session",
        tags=["session"]
    )

    new_app.include_router(
        user_router,
        prefix="/user",
        tags=["user"]
    )

    new_app.include_router(
        account_router,
        prefix="/account",
        tags=["account"]
    )

    new_app.include_router(
        rule_overview_router,
        prefix="/ruleOverview",
        tags=["rule overview"]
    )

    new_app.include_router(
        resource_router,
        prefix="/resource",
        tags=["resource"]
    )

    new_app.include_router(
        rule_router,
        prefix="/rule",
        tags=["rule"]
    )

    new_app.include_router(
        compliance_router,
        prefix="/compliance",
        tags=["compliance"]
    )

    new_app.include_router(
        exception_router,
        prefix="/exceptions",
        tags=["exceptions"]
    )

    new_app.include_router(
        account_overview_router,
        prefix="/accountOverview",
        tags=["account overview"]
    )

    new_app.include_router(
        exception_audit_router,
        prefix="/exceptionAudit",
        tags=["exception audit"]
    )

    new_app.include_router(
        search_router,
        prefix="/search",
        tags=["search"]
    )

    # Define OpenAPI info
    def custom_openapi():
        if new_app.openapi_schema:
            return new_app.openapi_schema
        openapi_schema = get_openapi(
            title="ITP API",
            description="AC41004 - Industrial Team Project: Team 1 API Backend",
            version="Alpha: 1.0.0",
            routes=new_app.routes,
            tags=[
                {
                    "name": "session",
                    "description": "User session management"
                },
                {
                    "name": "user",
                    "description": "User details"
                },
                {
                    "name": "account",
                    "description": "Account details"
                },
                {
                    "name": "rule",
                    "description": "Rule details"
                },
                {
                    "name": "compliance",
                    "description": "Compliance details"
                },
                {
                    "name": "rule overview",
                    "description": "Rule overview"
                },
                {
                    "name": "resource",
                    "description": "Resource details"
                },
                {
                    "name": "exceptions",
                    "description": "Rule Exceptions for resource"
                },
                {
                    "name": "account overview",
                    "description": "account overview stats"
                },
                {
                    "name": "exception audit",
                    "description": "Audit log for exception"
                },
                {
                    "name": "search",
                    "description": "Search engine"
                }
            ]
        )
        new_app.openapi_schema = openapi_schema
        return new_app.openapi_schema

    new_app.openapi = custom_openapi

    # Include Routes
    return new_app


app = create_app()
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=2000)
