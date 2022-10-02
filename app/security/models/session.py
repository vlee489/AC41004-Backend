from dataclasses import dataclass, InitVar, field


@dataclass
class UserSession:
    session_data: InitVar[dict]
    id: str = field(init=False, default="")

    email: str = field(init=False, default="")
    first_name: str = field(init=False, default="")
    last_name: str = field(init=False, default="")
    session_expiry: str = field(init=False, default="")

    role_id: str = field(init=False, default="")
    customer_id: str = field(init=False, default="")

    def __post_init__(self, session_data: dict):
        self.id = session_data.get("id", "")

        self.email = session_data.get("email", "")
        self.first_name = session_data.get("first_name", "")
        self.last_name = session_data.get("last_name", "")

        self.role_id = session_data.get("role_id", 0)
        self.customer_id = session_data.get("customer_id", "")
        self.session_expiry = session_data.get("session_expiry", "")
