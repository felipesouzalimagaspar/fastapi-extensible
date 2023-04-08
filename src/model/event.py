from src.model.entity import Entity
from src.model.device import Device
from src.model.thing import Thing
from enum import Enum
from datetime import datetime

class EventType(int, Enum):
    PERIODIC = 0
    CONDITIONAL = 1
    BY_HUMAN = 2
class ActionType(int, Enum):
    HTTP_REQUEST = 0
    SEND_SIGNAL = 1
    RECEIVE_SIGNAL = 2
    LOST_SIGNAL = 3
    API_CRUD = 4
    RUN_SCRIPT = 5
    NONE = 6
class Event(Entity):
    name: str
    description: str
    type: EventType
    causeType: ActionType
    cause: str
    actionType: ActionType
    action: str
    datetime: datetime
    topic: str | bool = False
    device: bool | Device = False
    thing: bool | Thing = False