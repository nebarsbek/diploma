from dataclasses import dataclass

@dataclass
class User:
    email: str
    password_hash: str
    id: int | None = None
    is_active: bool = True
    role: str = "employee"
    is_verified: bool = False