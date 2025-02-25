import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Multilingual Chat application"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Multilingual Chat application is healthy"}

def test_integration_spec():
    response = client.get("/integration-spec")
    assert response.status_code in [200, 404]

def test_translate_text():
    payload = {
        "message": "Hello",
        "settings": [
            {"label": "preferredLanguage", "default": "fr"}
        ]
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    json_response = response.json()
    print("Response:", json_response)
    assert "message" in json_response
    assert json_response["message"] != "Hello"

def test_translate_empty_message():
    payload = {"message": "", "settings": []}
    response = client.post("/webhook", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Message content cannot be empty"

def test_translate_invalid_language():
    payload = {
        "message": "Hello",
        "settings": [
            {"label": "preferredLanguage", "default": "xyz"}
        ]
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    json_response = response.json()
    print("Response:", json_response)
    assert json_response["message"] == "Error: Language not supported"