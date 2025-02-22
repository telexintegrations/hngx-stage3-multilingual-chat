from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List
import json
import os
from translate import Translator

app = FastAPI()

class Setting(BaseModel):
    label: str
    type: str
    default: str
    required: bool

class IncomingMessage(BaseModel):
    message: str
    settings: List[Setting]

class ResponseMessage(BaseModel):
    message: str

@app.post("/webhook", response_model=ResponseMessage)
async def modify_message(payload: IncomingMessage):
    incoming_message = payload.message
    settings = payload.settings
    
    target_language = "es"  # Example target language

    try:
        # Use the `translate` package for translation
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
        return JSONResponse({"message": "Integration spec not found"}, status_code=404)

@app.get("/health")
async def health_check():
    return {"message": "Multilingual Chat application is healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
