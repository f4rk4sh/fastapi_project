import random
import string
from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.config.superuser_config import superuser_cfg


def random_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


def random_integer() -> int:
    return random.randint(1, 9)


def random_special_symbol() -> str:
    return "".join(random.choices("!@#$%^&*()-_=+||\\", k=1))


def random_email() -> str:
    return f"{random_string()}@{random_string().lower()}.com"


def random_password() -> str:
    return f"{random_string().capitalize()}{random_integer()}{random_special_symbol()}"


def random_phone() -> str:
    return "+" + "".join([str(random_integer()) for _ in range(12)])


def random_date(in_future: bool = False):
    return (
        date.today() + timedelta(days=1)
        if in_future
        else date.today() - timedelta(days=-1)
    )


def get_su_token_headers(client: TestClient) -> dict:
    login_data = {
        "username": superuser_cfg.SU_EMAIL,
        "password": superuser_cfg.SU_PASSWORD,
    }
    response = client.post("/auth/login", data=login_data).json()
    access_token = response["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
