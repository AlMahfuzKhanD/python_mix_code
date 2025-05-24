import serial
import requests
import re
import time
import uuid
import os
import logging

# =================== CONFIG ===================
PORT = 'COM3'
BAUD_RATE = 9600
TIMEOUT = 1
API_URL = 'https://cserp.store/api/receive-weight'
HEADERS = {
    'User-Agent': 'WeightBridgeClient/1.0',
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

# =================== LOGGING ===================
logging.basicConfig(
    filename='weight_machine.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# =================== FUNCTIONS ===================

def get_machine_id():
    """Generate machine ID using MAC address (first 6 digits for uniqueness)."""
    mac = uuid.getnode()
    return ':'.join(['{:02x}'.format((mac >> ele) & 0xff) for ele in range(40, -1, -8)])

def extract_weights(data):
    """Extract and validate weights from raw serial data."""
    matches = re.findall(r'\x02([+-]\d{9})\x03', data)
    weights = [int(m) / 1000 for m in matches]

    # Filter out low noise values (below threshold)
    final_weights = []
    for weight in weights:
        if weight < 1.0:
            final_weights.append(0.00)
        else:
            final_weights.append(round(weight, 2))
    return final_weights

# =================== MAIN ===================

MACHINE_ID = get_machine_id()
print(f"🔧 Machine ID: {MACHINE_ID}")

last_sent_weight = None

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"✅ Connected to {PORT} at {BAUD_RATE} baud.")

    while True:
        if ser.in_waiting:
            raw = ser.read(40)
            decoded = raw.decode('utf-8', errors='ignore')
            weights = extract_weights(decoded)

            if weights:
                latest_weight = weights[-1]

                if latest_weight != last_sent_weight:
                    print(f"📤 Sending: {latest_weight} kg from Machine: {MACHINE_ID}")
                    logging.info(f"Sending: {latest_weight} from {MACHINE_ID}")
                    try:
                        response = requests.post(
                            API_URL,
                            data={
                                'weight': latest_weight,
                                'machine_id': MACHINE_ID
                            },
                            headers=HEADERS,
                            timeout=5
                        )
                        print("✅ Laravel responded:", response.text)
                        last_sent_weight = latest_weight
                    except Exception as e:
                        logging.error(f"❌ Error sending to Laravel: {e}")
                        print("❌ Error sending to Laravel:", e)
        else:
            time.sleep(0.1)

except serial.SerialException as se:
    print("🔌 Serial connection error:", se)
    logging.error(f"Serial error: {se}")

except KeyboardInterrupt:
    print("🛑 Script interrupted by user.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("🔌 Serial port closed.")
