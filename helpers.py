# Language code mapping
LANGUAGE_MAP = {
    "Afrikaans (Afrikaans)": "af",
    "Albanian (Shqip)": "sq",
    "Amharic (አማርኛ)": "am",
    "Arabic (العربية)": "ar",
    "Armenian (Հայերեն)": "hy",
    "Azerbaijani (Azərbaycanca)": "az",
    "Basque (Euskara)": "eu",
    "Belarusian (Беларуская)": "be",
    "Bengali (বাংলা)": "bn",
    "Bosnian (Bosanski)": "bs",
    "Bulgarian (Български)": "bg",
    "Catalan (Català)": "ca",
    "Cebuano (Cebuano)": "ceb",
    "Chichewa (Chichewa)": "ny",
    "Chinese (中文)": "zh",
    "Corsican (Corsu)": "co",
    "Croatian (Hrvatski)": "hr",
    "Czech (Čeština)": "cs",
    "Danish (Dansk)": "da",
    "Dutch (Nederlands)": "nl",
    "English (English)": "en",
    "Esperanto (Esperanto)": "eo",
    "Estonian (Eesti)": "et",
    "Filipino (Filipino)": "tl",
    "Finnish (Suomi)": "fi",
    "French (Français)": "fr",
    "Galician (Galego)": "gl",
    "Georgian (ქართული)": "ka",
    "German (Deutsch)": "de",
    "Greek (Ελληνικά)": "el",
    "Gujarati (ગુજરાતી)": "gu",
    "Haitian Creole (Kreyòl Ayisyen)": "ht",
    "Hausa (Hausa)": "ha",
    "Hawaiian (ʻŌlelo Hawaiʻi)": "haw",
    "Hebrew (עברית)": "iw",
    "Hindi (हिन्दी)": "hi",
    "Hmong (Hmoob)": "hmn",
    "Hungarian (Magyar)": "hu",
    "Icelandic (Íslenska)": "is",
    "Igbo (Asụsụ Igbo)": "ig",
    "Indonesian (Bahasa Indonesia)": "id",
    "Irish (Gaeilge)": "ga",
    "Italian (Italiano)": "it",
    "Japanese (日本語)": "ja",
    "Javanese (Basa Jawa)": "jv",
    "Kannada (ಕನ್ನಡ)": "kn",
    "Kazakh (Қазақ тілі)": "kk",
    "Khmer (ភាសាខ្មែរ)": "km",
    "Korean (한국어)": "ko"
}

def get_language_code(language_name):
    return LANGUAGE_MAP.get(language_name, "en")
