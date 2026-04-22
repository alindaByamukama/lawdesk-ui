import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def login(username: str, password: str) -> dict:
    try:
        response = requests.post(
            f"{BASE_URL}/auth/jwt/create/",
            json={"username": username, "password": password},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return {}
    except requests.exceptions.RequestException:
        return {}

def refresh_token(refresh: str) -> str | None:
    try:
        response = requests.post(
            f"{BASE_URL}/auth/jwt/refresh/",
            json={"refresh": refresh},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("access")
        return None
    except requests.exceptions.RequestException:
        return None