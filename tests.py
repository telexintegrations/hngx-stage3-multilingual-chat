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
    if response.status_code == 200:
        assert "data" in response.json()
    else:
        assert response.status_code == 404
        assert response.json() == {"detail": "Integration spec not found"}

def test_modify_message_default_translator():
    payload = {
        "message": "Hello, world!",
        "settings": [],
        "translator": "Default Translator",
        "target_language": "French (Français)"
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    assert "message" in response.json()

def test_modify_message_google_translator_missing_key():
    payload = {
        "message": "Hello, world!",
        "settings": [],
        "translator": "Google Translator",
        "target_language": "French (Français)",
        "google_api_key": ""
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Google API key is required for Google Translator"}

def test_modify_message_microsoft_translator_missing_key():
    payload = {
        "message": "Hello, world!",
        "settings": [],
        "translator": "Microsoft Translator",
        "target_language": "French (Français)",
        "microsoft_api_key": ""
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Microsoft API key is required for Microsoft Translator"}

def test_modify_message_empty_message():
    payload = {
        "message": "",
        "settings": [],
        "translator": "Default Translator",
        "target_language": "French (Français)"
    }
    response = client.post("/webhook", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Message content cannot be empty"}
