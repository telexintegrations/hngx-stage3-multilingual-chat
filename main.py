from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from translate import Translator
from helpers import get_language_code

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["Content-Type"],
)

# Valid languages
VALID_LANGUAGES = [
    "af", "sq", "am", "ar", "hy", "az", 
    "eu", "be", "bn", "bs", "bg", "ca", 
    "ceb", "ny", "zh", "co", "hr", "cs", 
    "da", "nl", "en", "eo", "et", "tl", 
    "fi", "fr", "gl", "ka", "de", "el", 
    "gu", "ht", "ha", "haw", "iw", "hi", 
    "hmn", "hu", "is", "ig", "id", "ga", 
    "it", "ja", "jv", "kn", "kk", "km", "ko"
    ]

class TranslationRequest(BaseModel):
    message: str
    settings: list[dict]

@app.post("/webhook")
async def translate_text(request: TranslationRequest):
    message = request.message.strip()
    target_language = "fr"
    
    # Parse settings to determine target language
    for setting in request.settings:
        find_language_code = get_language_code(setting.get("default"))
        if setting.get("label") == "preferredLanguage" and get_language_code in VALID_LANGUAGES:
            target_language = find_language_code
            break

    if not message:
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    try:
        translator = Translator(to_lang=target_language)
        translated_message = translator.translate(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

    # Print the selected language
    print(f"Selected language: {target_language} for message: {message} -> {translated_message}")

    return {"message": translated_message}

@app.get("/")
async def home():
    return {"message": "Welcome to Multilingual Chat application"}

@app.get("/integration-spec")
async def integration_spec():
    try:
        with open("integration_settings.json", "r") as file:
            integration_spec = json.load(file)
        return JSONResponse(integration_spec)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Integration spec not found")

@app.get("/health")
async def health_check():
    return {"message": "Multilingual Chat application is healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
