import unittest
import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)

from src.model.entity import Entity
from src.model.user import User
from src.model.user import UserType
from src.database.crud import CRUD
from config.bootstrap import start_app


class TestCRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        DATABASES, API = start_app()
        cls.crud = CRUD(DATABASES['master'])
        cls.redis_conn = DATABASES['master']
        cls.redis_conn.flushdb()

    @classmethod
    def tearDownClass(cls):
        cls.redis_conn.flushdb()

    def setUp(self):
        self.crud.truncate(User)

    def test_insert(self):
        user = User(name="Alice", mail="alice@example.com", password="secret", type=UserType.DEFAULT)
        key = self.crud.insert(user)
        self.assertTrue(self.redis_conn.exists(key))

    def test_update(self):
        user = User(name="Alice", mail="alice@example.com", password="secret", type=UserType.DEFAULT)
        key = self.crud.insert(user)
        updated_user = User(id=user.id, name="Alice Smith", mail="alice@example.com", password="secret", type=UserType.DEFAULT)
        self.crud.update(updated_user)
        json_data = self.redis_conn.get(key)
        self.assertIsNotNone(json_data)
        saved_user = User.parse_raw(json_data)
        self.assertEqual(saved_user.name, "Alice Smith")

    def test_delete(self):
        user = User(name="Alice", mail="alice@example.com", password="secret", type=UserType.DEFAULT)
        key = self.crud.insert(user)
        self.crud.delete(user)
        self.assertFalse(self.redis_conn.exists(key))

    def test_truncate(self):
        user1 = User(name="Alice", mail="alice@example.com", password="secret", type=UserType.DEFAULT)
        user2 = User(name="Bob", mail="bob@example.com", password="secret", type=UserType.DEFAULT)
        self.crud.insert(user1)
        self.crud.insert(user2)
        self.crud.truncate(User)
        keys = self.redis_conn.keys(User.generate_key() + ":*")
        self.assertEqual(len(keys), 0)

    def test_get(self):
        user = User(name="Alice", mail="alice@example.com", password="secret", type=UserType.DEFAULT)
        self.crud.insert(user)
        key = user.id
        saved_user = self.crud.get(User, key)
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.name, "Alice")

    def test_list(self):
        user1 = User(name="Alice", mail="alice@example.com", password="secret", type=UserType.DEFAULT)
        user2 = User(name="Bob", mail="bob@example.com", password="secret", type=UserType.DEFAULT)
        self.crud.insert(user1)
        self.crud.insert(user2)
        users = self.crud.list(User)
        self.assertEqual(len(users), 2)

    def test_count(self):
        user1 = User(name="Alice", mail="alice@example.com", password="secret", type=UserType.DEFAULT)
        user2 = User(name="Bob", mail="bob@example.com", password="secret", type=UserType.DEFAULT)
        self.crud.insert(user1)
        self.crud.insert(user2)
        count = self.crud.count(User)
        self.assertEqual(count, 2)
        
    def test_search(self):
        user1 = User(name="Alice", mail="alice@example.com", password="secret", type=UserType.DEFAULT)
        user2 = User(name="Bob", mail="bob@example.com", password="secret", type=UserType.DEFAULT)
        user3 = User(name="Charlie", mail="charlie@example.com", password="secret", type=UserType.DEFAULT)
        self.crud.insert(user1)
        self.crud.insert(user2)
        self.crud.insert(user3)
        search_results = self.crud.search(User, "name", "Charlie")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].name, "Charlie")

    
if __name__ == '__main__':
    unittest.main()
