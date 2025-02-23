from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# from deep_translator import Translator
import json
from translate import Translator

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["Content-Type"],
)

# Valid languages
VALID_LANGUAGES = ["en", "es", "fr", "de", "it", "ja", "zh"]

class TranslationRequest(BaseModel):
    message: str
    settings: list[dict]

@app.post("/webhook", response_model=ResponseMessage)
async def translate_text(request: TranslationRequest):
    message = request.message.strip()
    target_language = "fr"  # Default language

    # Parse settings
    for setting in request.settings:
        if setting.get("label") == "preferredLanguage" and setting.get("default") in VALID_LANGUAGES:
            target_language = setting.get("default")
            break

    if not message:
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    try:
        translator = Translator(target=target_language)
        translated_message = translator.translate(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

    return {"translated_message": translated_message, "language": target_language}

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
