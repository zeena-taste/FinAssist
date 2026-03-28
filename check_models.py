import requests
from app.config import settings

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={settings.GEMINI_API_KEY}"
response = requests.get(url)
print(response.status_code)
try:
    models = response.json()
    for m in models.get("models", []):
        print(m["name"])
except Exception as e:
    print(response.text)
