from src.model.entity import Entity
from src.model.local import Local
from src.model.device import Device

class Thing(Entity):
    name: str
    local: Local
    device: Device