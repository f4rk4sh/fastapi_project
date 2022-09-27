import random
import string

from fastapi.testclient import TestClient

from app.config.su_config import SUConfig


def random_string(length: int = 10):
    return "".join(random.choices(string.ascii_letters, k=length))


def random_integer():
    return random.randint(1, 9)


def get_su_token_headers(client: TestClient):
    login_data = {
        "username": SUConfig.SU_EMAIL,
        "password": SUConfig.SU_PASSWORD,
    }
    response = client.post("/auth/login", data=login_data).json()
    access_token = response["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
