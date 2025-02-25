# Multilingual Chat: A Telex Modifier Integration

## 📌 Introduction
This integration automatically translates incoming messages to a specified language. It detects the language of incoming messages and translates them into the user's selected language, making communication more inclusive and accessible. Built as a Modifier Integration for Telex, it ensures seamless multilingual interaction within Telex channels.

---

## Integration Overview
I built a Modifier Integration, leveraging Telex's integration types:

1. *Modifier Integrations*: Modify new messages entering a channel (e.g., profanity filter, text translator).
2. *Interval Integrations*: Send messages to a channel at set intervals (e.g., Bitcoin price tracker, website uptime monitor).
3. *Output Integrations*: Route data from a Telex channel to external services (e.g., email notifications, Discord webhooks).

This integration follows Telex's documentation and best coding practices.

---

## 🚀 Features
- *Automatic Language Detection*: Identifies the source language of incoming messages.
- *Real-time Translation*: Translates messages to the user's preferred language.
- *Seamless Integration*: Works within Telex channels without manual intervention.
- *Error Handling*: Gracefully handles unsupported languages and other translation errors.

---

## 🔧 Setup Instructions

### 1. Clone the Repository
bash
# Clone this repository
git clone [hngx-stage3-multilingual-chat](https://github.com/telexintegrations/hngx-stage3-multilingual-chat.git)
cd hngx-stage3-multilingual-chat


### 2. Create a Virtual Environment
bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


### 3. Install Dependencies
bash
pip install -r requirements.txt




### 4. Run the FastAPI Server
bash
uvicorn main:app --reload --port 8000


---

## Testing

### Run Tests
Ensure all test cases pass before deployment:
bash
pytest tests.py


### Example Test Cases
- *test_translate_text*: Ensures messages are correctly translated.
- *test_translate_invalid_language*: Validates error handling for unsupported languages.
- *test_webhook_response*: Checks if the webhook returns the correct JSON responses.

---

## Deployment

### Deploy to AWS EC2
1. *SSH into your EC2 instance:*
bash
ssh -i your-key.pem ubuntu@your-ec2-ip

2. *Install Docker:*
bash
sudo apt update
sudo apt install docker.io

3. *Build and Run the Docker container:*
bash
docker build -t multilingual-chat .
docker run -d -p 8000:8000 multilingual-chat

4. *Set up Nginx for Reverse Proxy:*
Ensure your FastAPI app is accessible publicly:
bash
sudo nano /etc/nginx/sites-available/multilingual_chat

Add the following configuration:
nginx
server {
    listen 80;
    server_name your-ec2-ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

Enable the configuration and restart Nginx:
bash
sudo ln -s /etc/nginx/sites-available/multilingual_chat /etc/nginx/sites-enabled/
sudo systemctl restart nginx


---

## How to Use the Integration

1. *Add the Integration to Your Telex Channel:*
   - Go to your Telex dashboard.
   - Navigate to *Integrations* via the *Apps* > *Add New Integration*.
   - Enter your *Integration JSON Url*.
2. *Configure the Integration:*
   - Set the webhook URL to your FastAPI app (e.g., http://your-ec2-ip/webhook).
   - Choose the preferred language in the settings.
3. *Test the Integration:*
   - Send a message in any language to your Telex channel.
   - Watch it auto-translate to the configured language!

---

## Screenshots

Screenshots of the integration on Telex Test Org. 4 Multilingual-Chat Channel

1. *Incoming Message Detected*
![image](https://github.com/user-attachments/assets/1503c4d7-f4e9-477a-962b-a3acdd30a5c8)





2. *Language Detected and Translated*
![image](https://github.com/user-attachments/assets/945c478f-e186-4eab-b5c7-8da461b5ae41)




3. *Telex Channel Output*
![image](https://github.com/user-attachments/assets/0b8b6a0b-8329-4fa6-a29c-f7913fcf2c43)


---


### Functionality
- Integration works as described in the Telex documentation.
- Properly modifies messages using the Modifier type.


### Code Quality
- Clean, maintainable, and well-documented code.
- Effective error handling and input validation.

