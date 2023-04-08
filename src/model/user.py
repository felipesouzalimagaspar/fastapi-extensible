from src.model.entity import Entity
from enum import Enum

class UserType(int, Enum):
    ADMIN = 1
    DEFAULT = 0
class User(Entity):
    name: str
    mail: str
    password: str
    type: UserType