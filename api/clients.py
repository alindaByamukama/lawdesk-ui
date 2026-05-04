import os
from dotenv import load_dotenv
from utils.session import authenticated_request

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def get_clients(search: str = None) -> dict | None:
    params = {}
    if search:
        params["search"] = search
    return authenticated_request("get", f"{BASE_URL}/api/clients/", params=params)


def create_client(payload: dict) -> dict | None:
    return authenticated_request("post", f"{BASE_URL}/api/clients/", json=payload)


def get_client(client_id: int) -> dict | None:
    return authenticated_request("get", f"{BASE_URL}/api/clients/{client_id}/")