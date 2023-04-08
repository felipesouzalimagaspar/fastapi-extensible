import json
import hashlib
from uuid import uuid4
from pydantic import BaseModel

class Entity(BaseModel):
    id: str = ""
    disabled: bool = False
    excluded: bool = False

    def __init__(self, **data):
        if 'id' not in data:
            classname = self.__class__.__name__
            data['id'] = f"{classname}:{hashlib.sha256(str(uuid4()).encode()).hexdigest()}"
        if 'disabled' not in data:
            data['disabled'] = False
        if 'excluded' not in data:
            data['excluded'] = False
        super().__init__(**data)

    def to_json(self):
        return self.json()

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    @classmethod
    def generate_key(cls):
        return cls.__name__
