BASE_URL = "https://api.pomidor-stage.ru"

AUTH_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
    }

API_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
    }

AUTH_DATA = {
    "username": "xamidullin12@mail.ru",
    "password": "lenar999",
    "scope": "",
    "client_id": "",
    "client_secret": ""
    }

def get_auth_token():
    response = requests.post(LOGIN_URL, data=AUTH_DATA, headers=HEADERS)
    assert response.status_code == 200
    return response.json().get("access_token")

def create_item(title, description, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    data = {
        "title": title,
        "description": description
    }
    response = requests.post(ITEMS_URL, json=data, headers=headers)
    assert response.status_code in (200, 201)
    item = response.json()
    print(f"{item['title']} (ID: {item['id']})")

    if __name__ == "__main__":
        token = get_auth_token()
        for i in range(20):
            create_item(f"Test Item {i}", f"Description {i}", token)