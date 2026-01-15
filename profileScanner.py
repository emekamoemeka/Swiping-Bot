import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FACEPP_API_KEY")
API_SECRET = os.getenv("FACEPP_API_SECRET")

url = "https://api-us.faceplusplus.com/facepp/v3/detect"

data = {
    "api_key": API_KEY,
    "api_secret": API_SECRET,
    "return_attributes": "beauty,smiling,headpose"
}

with open("faces/emeka.png", "rb") as f:
    files = {
        "image_file": f
    }
    response = requests.post(url, data=data, files=files)

print(response.json()['faces'][0]['attributes']['beauty'])