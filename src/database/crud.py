from typing import List
from src.model.entity import Entity
import redis


class CRUD:
    def __init__(self, connection: redis.Redis):
        self.connection = connection

    def insert(self, entity: Entity) -> str:
        key = entity.id
        json_data = entity.to_json()
        self.connection.set(key, json_data)
        return key

    def update(self, entity: Entity) -> bool:
        key = entity.id
        if self.connection.exists(key):
            json_data = entity.to_json()
            self.connection.set(key, json_data)
            return True
        else:
            return False

    def delete(self, entity: Entity) -> bool:
        key = entity.id
        if self.connection.exists(key):
            if self.connection.delete(key):
                return True
            else:
                return False
        else:
            return False

    def truncate(self, entity_class: type) -> None:
        entity_key_pattern = f"{entity_class.__name__}:*"
        keys = self.connection.keys(entity_key_pattern)
        for key in keys:
            self.connection.delete(key)

    def get(self, entity_class: type, unique_key: str) -> Entity:
        json_data = self.connection.get(unique_key)
        if json_data:
            entity = entity_class.from_json(json_data)
            if entity.excluded:
                return None
            return entity
        else:
            return None

    def list(self, entity_class: type, page: int = 1, per_page: int = 10) -> List[Entity]:
        entity_key_pattern = f"{entity_class.__name__}:*"
        keys = self.connection.scan_iter(entity_key_pattern)
        entities = []
        start_index = (page - 1) * per_page
        end_index = start_index + per_page - 1
        for index, key in enumerate(keys):
            if start_index <= index <= end_index:
                json_data = self.connection.get(key)
                entity = entity_class.from_json(json_data)
                if entity.excluded:
                    continue
                entities.append(entity)
        return entities

    def count(self, entity_class: type) -> int:
        entity_key_pattern = f"{entity_class.__name__}:*"
        keys = self.connection.keys(entity_key_pattern)
        return len(keys)

    def search(self, entity_class: type, attribute: str, value) -> List[Entity]:
        entity_key_pattern = f"{entity_class.__name__}:*"
        keys = self.connection.scan_iter(entity_key_pattern)
        entities = []
        for key in keys:
            json_data = self.connection.get(key)
            entity = entity_class.from_json(json_data)
            if getattr(entity, attribute) == value:
                if entity.excluded:
                    continue
                entities.append(entity)
        return entities
