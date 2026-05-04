import os
from dotenv import load_dotenv
from utils.session import authenticated_request

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def get_cases(status: str = None, search: str = None,
              next_hearing_gte: str = None, next_hearing_lte: str = None, ordering: str = None) -> dict | None:
    params = {}
    if status:
        params["status"] = status
    if search:
        params["search"] = search
    if next_hearing_gte:
        params["next_hearing_date__gte"] = next_hearing_gte
    if next_hearing_lte:
        params["next_hearing_date__lte"] = next_hearing_lte
    if ordering:
        params["ordering"] = ordering

    return authenticated_request("get", f"{BASE_URL}/api/cases/", params=params)


def get_case(case_id: int) -> dict | None:
    return authenticated_request("get", f"{BASE_URL}/api/cases/{case_id}/")


def create_case(payload: dict) -> dict | None:
    return authenticated_request("post", f"{BASE_URL}/api/cases/", json=payload)


def update_case_status(case_id: int, status: str) -> dict | None:
    return authenticated_request("patch", f"{BASE_URL}/api/cases/{case_id}/status/",
                                  json={"status": status})