import serial
import requests
import re
import time
import uuid  # 🔸 For getting MAC address

# Configuration
PORT = 'COM3'
BAUD_RATE = 9600
TIMEOUT = 1
# API_URL = 'https://cserp.store/api/receive-weight'
API_URL = 'http://127.0.0.1:8000/api/receive-weight'

# Custom headers to help bypass ModSecurity
HEADERS = {
    'User-Agent': 'WeightBridgeClient/1.0',
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

# ✅ Generate machine ID using MAC address
def get_machine_id():
    mac = uuid.getnode()
    return ':'.join(['{:02x}'.format((mac >> ele) & 0xff) for ele in range(40, -1, -8)])

MACHINE_ID = get_machine_id()
print(f"🔧 Machine ID: {MACHINE_ID}")

def extract_weights(data):
    matches = re.findall(r'\x02([+-]\d{9})\x03', data)
    return [f"{int(m)/1000:.3f}" for m in matches]

last_sent_weight = None

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"✅ Connected to {PORT}")

    while True:
        if ser.in_waiting:
            raw = ser.read(40)
            decoded = raw.decode('utf-8', errors='ignore')
            weights = extract_weights(decoded)

            if weights:
                latest_weight = weights[-1]  # Use the last detected weight

                if latest_weight != last_sent_weight:
                    print(f"📤 Sending: {latest_weight} from Machine: {MACHINE_ID}")
                    try:
                        response = requests.post(
                            API_URL,
                            data={
                                'weight': latest_weight,
                                'machine_id': MACHINE_ID
                            },
                            headers=HEADERS,
                            verify=True
                        )
                        print("✅ Laravel responded:", response.text)
                        last_sent_weight = latest_weight
                    except Exception as e:
                        print("❌ Error sending to Laravel:", e)
        else:
            time.sleep(0.1)

except serial.SerialException as se:
    print("🔌 Serial connection error:", se)

except KeyboardInterrupt:
    print("🛑 Script interrupted by user.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("🔌 Serial port closed.")
