from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
from translate import Translator
from deep_translator import GoogleTranslator, MicrosoftTranslator

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
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
    message: str = Field(..., min_length=1, max_length=1000)
    settings: List[Setting]
    translator: Optional[str] = "Default Translator"
    target_language: Optional[str] = "English"
    google_api_key: Optional[str] = None
    microsoft_api_key: Optional[str] = None

class ResponseMessage(BaseModel):
    message: str

# Language code mapping
LANGUAGE_CODES = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Portuguese": "pt",
    "Russian": "ru"
}

def get_language_code(language_name):
    return LANGUAGE_CODES.get(language_name, "en")

def translate_message(translator_type, incoming_message, target_language, google_api_key=None, microsoft_api_key=None):
    try:
        if translator_type == "Google Translator":
            if not google_api_key:
                raise ValueError("Google API key is required for Google Translator")
            translated_message = GoogleTranslator(source='auto', target=target_language, api_key=google_api_key).translate(incoming_message)

        elif translator_type == "Microsoft Translator":
            if not microsoft_api_key:
                raise ValueError("Microsoft API key is required for Microsoft Translator")
            translated_message = MicrosoftTranslator(source='auto', target=target_language, api_key=microsoft_api_key).translate(incoming_message)

        else:
            translator = Translator(to_lang=target_language)
            translated_message = translator.translate(incoming_message)
        
        return translated_message
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook", response_model=ResponseMessage)
async def modify_message(payload: IncomingMessage):
    incoming_message = payload.message
    translator_type = payload.translator
    target_language_name = payload.target_language

    # Validate target language
    if target_language_name not in LANGUAGE_CODES:
        raise HTTPException(status_code=400, detail="Unsupported target language")
    
    target_language = get_language_code(target_language_name)
    google_api_key = payload.google_api_key
    microsoft_api_key = payload.microsoft_api_key

    try:
        modified_message = translate_message(translator_type, incoming_message, target_language, google_api_key, microsoft_api_key)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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
