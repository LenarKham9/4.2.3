import pytest
from constant import BASE_URL


class TestItems:
    endpoint = f"{BASE_URL}/api/v1/items/"

    def test_create_item(self, item_data, auth_session):
        response = auth_session.post(self.endpoint, json=item_data)
        assert response.status_code in (200, 201), f"Response: {response.status_code}, {response.text}"

        data = response.json()
        item_id = data.get("id")
        assert item_id is not None
        assert data.get("title") == item_data["title"]

        self.created_item_id = item_id

    def test_get_items(self, auth_session):
        response = auth_session.get(self.endpoint)
        assert response.status_code == 200, f"Response: {response.status_code}, {response.text}"

        data = response.json()
        assert "data" in data, "Response missing 'data' key"
        assert isinstance(data["data"], list), "'data' is not a list"
        assert isinstance(data.get("count"), int), "'count' should be integer"

    def test_get_items_structure(self, auth_session):
        response = auth_session.get(self.endpoint)
        assert response.status_code == 200, f"Response: {response.status_code}, {response.text}"
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert isinstance(data.get("count"), int)

    def test_get_items_with_filters(self, auth_session):
        params = {"page": 1, "limit": 5, "sort": "title"}
        response = auth_session.get(self.endpoint, params=params)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_update_item(self, auth_session, created_item, item_data):
        # Обновляем созданный элемент
        new_title = "Обновленный " + item_data["title"]
        response = auth_session.put(f"{self.endpoint}{created_item}", json={
            "title": new_title,
            "description": item_data["description"]
        })
        assert response.status_code == 200
        updated = response.json()
        assert updated["title"] == new_title

    def test_delete_item(self, auth_session):
        # Создаем элемент для удаления
        response_create = auth_session.post(self.endpoint, json={"title": "Для удаления"})
        item_id = response_create.json()["id"]
        response_delete = auth_session.delete(f"{self.endpoint}{item_id}")
        assert response_delete.status_code in (200, 204)

        # Проверяем, что элемент удален
        response_get = auth_session.get(f"{self.endpoint}{item_id}")
        assert response_get.status_code == 404