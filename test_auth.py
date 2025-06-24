import pytest
from constant import BASE_URL, AUTH_HEADERS, AUTH_DATA

def test_authentication(auth_session):
    # Проверяем, что авторизация прошла успешно и токен получен
    response = auth_session.post(f"{BASE_URL}/api/v1/login/access-token", data=AUTH_DATA, headers=AUTH_HEADERS)
    assert response.status_code == 200, f"Auth failed with status {response.status_code}: {response.text}"
    json_response = response.json()
    assert "access_token" in json_response, "Нет access_token в ответе"
    token = json_response["access_token"]
    assert token, "access_token пустой"

    # Проверяем, что токен можно использовать для авторизации в API
    # Например, делаем запрос к защищенному эндпоинту
    headers = {"Authorization": f"Bearer {token}"}
    test_response = auth_session.get(f"{BASE_URL}/api/v1/items/", headers=headers)
    # Предположим, есть такой защищенный эндпоинт, или используйте существующий
    assert test_response.status_code == 200, "Доступ к защищенному эндпоинту не получен"

