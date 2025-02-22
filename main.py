from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List, Optional
import json
import os
from translate import Translator
from deep_translator import GoogleTranslator, MicrosoftTranslator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

class Setting(BaseModel):
    label: str
    type: str
    default: str
    required: bool

class IncomingMessage(BaseModel):
    message: str
    settings: List[Setting]
    translator: Optional[str] = "default"
    target_language: Optional[str] = "fr"
    google_api_key: Optional[str] = None
    microsoft_api_key: Optional[str] = None

class ResponseMessage(BaseModel):
    message: str

@app.post("/webhook", response_model=ResponseMessage)
async def modify_message(payload: IncomingMessage):
    incoming_message = payload.message
    translator_type = payload.translator
    target_language_name = payload.target_language
    target_language = target_language_name
    google_api_key = payload.google_api_key
    microsoft_api_key = payload.microsoft_api_key

    try:
        if not incoming_message:
            raise HTTPException(status_code=400, detail="Message content cannot be empty")

        if translator_type == "google":
            if not google_api_key:
                raise HTTPException(status_code=400, detail="Google API key is required for Google Translator")
            modified_message = GoogleTranslator(source='auto', target=target_language, api_key=google_api_key).translate(incoming_message)

        elif translator_type == "microsoft":
            if not microsoft_api_key:
                raise HTTPException(status_code=400, detail="Microsoft API key is required for Microsoft Translator")
            modified_message = MicrosoftTranslator(source='auto', target=target_language, api_key=microsoft_api_key).translate(incoming_message)

        else:
            translator = Translator(to_lang=target_language)
            modified_message = translator.translate(incoming_message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        raise HTTPException(status_code=404, detail="Integration spec not found")

@app.get("/health")
async def health_check():
    return {"message": "Multilingual Chat application is healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
