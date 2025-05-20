import serial
import time
import requests
import re

PORT = 'COM3'
BAUD_RATE = 9600
LARAVEL_ENDPOINT = 'http://127.0.0.1:8000/api/receive-weight'  # change as needed

def extract_weights(data):
    matches = re.findall(r'\x02([+-]\d{9})\x03', data)
    return [f"{int(m)/1000:.3f}" for m in matches]

ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
print(f"Connected to {PORT}")

while True:
    if ser.in_waiting:
        raw = ser.read(40)
        decoded = raw.decode('utf-8', errors='ignore')
        weights = extract_weights(decoded)
        for w in weights:
            print(f"Sending: {w} kg")
            try:
                res = requests.post(LARAVEL_ENDPOINT, data={
                    'weight': w,
                    'source': 'python-script'
                })
                print(f"✔️ Laravel responded: {res.text}")
            except Exception as e:
                print(f"❌ Failed to send: {e}")
    else:
        time.sleep(0.1)
