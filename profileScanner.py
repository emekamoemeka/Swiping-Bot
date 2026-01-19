import requests
import os
from dotenv import load_dotenv
from PIL import ImageGrab
import io

load_dotenv()

API_KEY = os.getenv("FACEPP_API_KEY")
API_SECRET = os.getenv("FACEPP_API_SECRET")

url = "https://api-us.faceplusplus.com/facepp/v3/detect"

data = {
    "api_key": API_KEY,
    "api_secret": API_SECRET,
    "return_attributes": "beauty,smiling,headpose"
}


x1, y1 = 990, 128 
x2, y2 = 1541, 838

screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

img_byte_arr = io.BytesIO()
screenshot.save(img_byte_arr, format='PNG')
img_byte_arr.seek(0)

files = {
    "image_file": img_byte_arr
}
response = requests.post(url, data=data, files=files)

emekas_list_of_interets = ["content creation", "NBA", "thrifting", "museums", "foodie", "bars", "basketball", "rap", "R&B", "Travel"]
age_range = (20, 25)

print(response.json()['faces'][0]['attributes']['beauty'])