from src.model.entity import Entity
from enum import Enum

class DeviceType(int, Enum):
    ACTIVE = 1
    PASSIVE = 0
class Device(Entity):
    name: str
    description: str
    datasheet: str
    input: bool
    output: bool
    type: DeviceType