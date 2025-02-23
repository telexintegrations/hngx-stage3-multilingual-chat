from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from translate import Translator

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

@app.post("/webhook")
async def translate_text(request: TranslationRequest):
    message = request.message.strip()
    target_language = "fr"
    
    # Parse settings to determine target language
    for setting in request.settings:
        if setting.get("label") == "preferredLanguage" and setting.get("default") in VALID_LANGUAGES:
            target_language = setting.get("default")
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

    return translated_message

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
