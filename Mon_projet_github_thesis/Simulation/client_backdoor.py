import requests
import time

url = "http://127.0.0.1:5001/firmware"

for _ in range(5):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            print("Update OK")
        else:
            print("Failed")
    except Exception as e:
        print("Error:", e)
    time.sleep(1)