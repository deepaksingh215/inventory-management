import unittest
from fastapi.testclient import TestClient
from main import app
from db import SessionLocal, Base, engine
from models import Item

client = TestClient(app)


class TestItems(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_create_item(self):
        response = client.post(
            "/api/v1/items/",
            json={"name": "TestItem", "description": "Test Description"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "TestItem")

    def test_read_item(self):
        item = Item(name="TestItem", description="Test Description")
        self.db.add(item)
        self.db.commit()
        response = client.get(f"/api/v1/items/{item.id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "TestItem")

    def test_update_item(self):
        item = Item(name="TestItem", description="Test Description")
        self.db.add(item)
        self.db.commit()
        response = client.put(
            f"/api/v1/items/{item.id}",
            json={"name": "UpdatedItem", "description": "Updated Description"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "UpdatedItem")

    def test_delete_item(self):
        item = Item(name="TestItem", description="Test Description")
        self.db.add(item)
        self.db.commit()
        response = client.delete(f"/api/v1/items/{item.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Item deleted successfully")


if __name__ == "__main__":
    unittest.main()
