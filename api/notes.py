import os
from dotenv import load_dotenv
from utils.session import authenticated_request

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def get_notes(case_id: int) -> dict | None:
    return authenticated_request("get", f"{BASE_URL}/api/cases/{case_id}/notes/list/")


def add_note(case_id: int, body: str) -> dict | None:
    return authenticated_request("post", f"{BASE_URL}/api/cases/{case_id}/quick_note/",
                                  json={"body": body})


def delete_note(note_id: int) -> bool:
    result = authenticated_request("delete", f"{BASE_URL}/api/notes/{note_id}/")
    return result is not None