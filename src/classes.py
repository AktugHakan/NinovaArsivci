from dataclasses import dataclass
# ---Classes---
@dataclass(slots=True)
class User:
    username: str
    password: str