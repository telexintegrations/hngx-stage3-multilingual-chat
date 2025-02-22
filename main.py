from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List, Optional
import json
import os
from translate import Translator
from deep_translator import GoogleTranslator, MicrosoftTranslator
from helpers import get_language_code

app = FastAPI()

class Setting(BaseModel):
    label: str
    type: str
    default: str
    required: bool

class IncomingMessage(BaseModel):
    message: str
    settings: List[Setting]
    translator: Optional[str] = "default"
    target_language: Optional[str] = "French (Français)"
    google_api_key: Optional[str] = None
    microsoft_api_key: Optional[str] = None

class ResponseMessage(BaseModel):
    message: str

@app.post("/webhook", response_model=ResponseMessage)
async def modify_message(payload: IncomingMessage):
    incoming_message = payload.message
    settings = payload.settings
    translator_type = payload.translator
    target_language_name = payload.target_language
    target_language = get_language_code(target_language_name)
    google_api_key = payload.google_api_key
    microsoft_api_key = payload.microsoft_api_key

    try:
        if translator_type == "google":
            if not google_api_key:
                return ResponseMessage(message="Input your Google API key")
            modified_message = GoogleTranslator(source='auto', target=target_language, api_key=google_api_key).translate(incoming_message)

        elif translator_type == "microsoft":
            if not microsoft_api_key:
                return ResponseMessage(message="Input your Microsoft API key")
            modified_message = MicrosoftTranslator(source='auto', target=target_language, api_key=microsoft_api_key).translate(incoming_message)

        else:
            translator = Translator(to_lang=target_language)
            modified_message = translator.translate(incoming_message)

    except Exception as e:
        return ResponseMessage(message=str(e))

    return ResponseMessage(message=modified_message)

@app.get("/")
async def home():
    return {"message": "Welcome to Multilingual Chat application"}

@app.get("/integration-spec")
async def integration_spec():
    try:
        with open("integration_settings.json", "r") as dmb:
            integration_spec = json.load(dmb)
        return JSONResponse(integration_spec)
    except FileNotFoundError:
        return JSONResponse({"message": "Integration settings not found"})