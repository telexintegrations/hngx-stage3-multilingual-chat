import requests
import uuid

def translate_text_google(text: str, target_language: str) -> str:
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        'q': text,
        'target': target_language,
        'format': 'text',
        'source': 'auto',
        'key': 'YOUR_GOOGLE_API_KEY'
    }
    
    response = requests.post(url, params=params)
    result = response.json()
    
    if response.status_code == 200 and 'data' in result:
        return result['data']['translations'][0]['translatedText']
    else:
        raise Exception("Error in translation: {}".format(result.get('error', 'Unknown error')))


def translate_text_microsoft(text: str, target_language: str) -> str:
    subscription_key = "YOUR_AZURE_SUBSCRIPTION_KEY"
    endpoint = "https://api.cognitive.microsofttranslator.com/translate"
    
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    
    params = {
        'api-version': '3.0',
        'to': [target_language]
    }
    
    body = [{
        'text': text
    }]
    
    response = requests.post(endpoint, params=params, headers=headers, json=body)
    result = response.json()
    
    if response.status_code == 200 and result:
        return result[0]['translations'][0]['text']
    else:
        raise Exception("Error in translation: {}".format(result.get('error', 'Unknown error')))


