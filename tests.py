import unittest
from chat_translator import translate_text_google, translate_text_microsoft

class TestTranslation(unittest.TestCase):

    def test_google_translation(self):
        text = "Hello, world!"
        target_language = "es"
        translated_text = translate_text_google(text, target_language)
        self.assertEqual(translated_text, "¡Hola, mundo!")

    def test_microsoft_translation(self):
        text = "Hello, world!"
        target_language = "es"
        translated_text = translate_text_microsoft(text, target_language)
        self.assertEqual(translated_text, "¡Hola, mundo!")

if __name__ == '__main__':
    unittest.main()
