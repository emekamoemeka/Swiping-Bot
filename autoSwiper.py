

from pynput.mouse import Button, Controller
import time
import requests
import os
from dotenv import load_dotenv
from PIL import ImageGrab
import io
import easyocr
import numpy as np

load_dotenv()

mouse = Controller()
emekas_list_of_interets = ["content creation", "NBA", "thrifting", "museums", "foodie", "bars", "basketball", "rap", "R&B", "Travel"]


dislike = (1189, 1025)
like = (1346, 1017)
skip = (1503, 554)

x1, y1 = 990, 128
x2, y2 = 1541, 838

ix1, iy1 = 975, 964
ix2, iy2 = 1527, 994

API_KEY = os.getenv("FACEPP_API_KEY")
API_SECRET = os.getenv("FACEPP_API_SECRET")
url = "https://api-us.faceplusplus.com/facepp/v3/detect"

ocr_reader = easyocr.Reader(['en'], gpu=False)

def analyze_profile():
    """Take screenshot and analyze beauty score"""
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

    img_byte_arr = io.BytesIO()
    screenshot.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    data = {
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "return_attributes": "beauty"
    }

    files = {
        "image_file": img_byte_arr
    }

    try:
        response = requests.post(url, data=data, files=files, timeout=10)
        result = response.json()

        if "faces" in result and len(result["faces"]) > 0:
            beauty = result["faces"][0]["attributes"]["beauty"]
            male_score = beauty["male_score"]
            female_score = beauty["female_score"]
            average_score = (male_score + female_score) / 2

            print(f"Male: {male_score}, Female: {female_score}, Average: {average_score:.2f}")
            return average_score
        else:
            print("No face detected")
            return 0

    except Exception as e:
        print("Face++ error:", e)
        return 0

def go_to_interests():
    """Click skip twice to reach interests page"""
    for _ in range(2):
        mouse.position = skip
        mouse.click(Button.left, 1)
        time.sleep(1.2)

def read_interests():
    screenshot = ImageGrab.grab(bbox=(ix1, iy1, ix2, iy2))

    screenshot = screenshot.convert("L")  

    img_np = np.array(screenshot)

    results = ocr_reader.readtext(img_np)

    if not results:
        print("No text detected in interests region")
        return []

    interests = []
    print("Detected interests:")

    for (_, text, confidence) in results:
        if confidence > 0.4:
            interests.append(text)
            print(f"- {text} (conf {confidence:.2f})")

    return interests

def has_matching_interest(detected_interests):
    """Check if any detected interests match Emeka's list"""
    for interest in detected_interests:
        for emeka_interest in emekas_list_of_interets:
            if emeka_interest.lower() in interest.lower() or interest.lower() in emeka_interest.lower():
                print(f"✓ MATCH FOUND: '{interest}' matches '{emeka_interest}'")
                return True
    return False

while True:
    score = analyze_profile()
    print("Score =", score)

    go_to_interests()

    interests = read_interests()

    has_match = has_matching_interest(interests)
    
    if score > 50 and has_match:
        print("✓ Swiping RIGHT (Good score + Matching interest)")
        mouse.position = like
    else:
        if score <= 50:
            print(f"✗ Swiping LEFT (Low score: {score})")
        elif not has_match:
            print("✗ Swiping LEFT (No matching interests)")
        else:
            print("✗ Swiping LEFT")
        mouse.position = dislike

    mouse.click(Button.left, 1)
    
    print("Waiting 10 seconds...\n")
    time.sleep(10)
