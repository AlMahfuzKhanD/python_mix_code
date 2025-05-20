# import serial
# import requests
# import re
# import time

# # Adjust these for your setup
# PORT = 'COM3'
# BAUD_RATE = 9600
# TIMEOUT = 1
# API_URL = 'http://127.0.0.1:8000/api/receive-weight'

# def extract_weights(data):
#     matches = re.findall(r'\x02([+-]\d{9})\x03', data)
#     return [f"{int(m)/1000:.3f}" for m in matches]

# try:
#     ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
#     print(f"✅ Connected to {PORT}")

#     while True:
#         if ser.in_waiting:
#             raw = ser.read(40)
#             decoded = raw.decode('utf-8', errors='ignore')
#             weights = extract_weights(decoded)

#             for weight in weights:
#                 print(f"Sending: {weight}")
#                 try:
#                     response = requests.post(API_URL, data={'weight': weight})
#                     print("Laravel responded:", response.text)
#                 except Exception as e:
#                     print("Error sending to Laravel:", e)
#         else:
#             time.sleep(0.5)

# except KeyboardInterrupt:
#     print("🔌 Script stopped by user.")

# finally:
#     if 'ser' in locals() and ser.is_open:
#         ser.close()
#         print("🔌 Serial port closed.")


# current code
import serial
import requests
import re
import time

# Adjust these for your setup
PORT = 'COM3'
BAUD_RATE = 9600
TIMEOUT = 1
API_URL = 'http://127.0.0.1:8000/api/receive-weight'

def extract_weights(data):
    matches = re.findall(r'\x02([+-]\d{9})\x03', data)
    return [f"{int(m)/1000:.3f}" for m in matches]

last_sent_weight = None  # Track the last weight sent

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"✅ Connected to {PORT}")

    while True:
        if ser.in_waiting:
            raw = ser.read(40)
            decoded = raw.decode('utf-8', errors='ignore')
            weights = extract_weights(decoded)

            if weights:
                latest_weight = weights[-1]  # Get only the most recent weight

                # ✅ Only send if the weight changed
                if latest_weight != last_sent_weight:
                    print(f"📤 Sending: {latest_weight}")
                    try:
                        response = requests.post(API_URL, data={'weight': latest_weight})
                        print("✅ Laravel responded:", response.text)
                        last_sent_weight = latest_weight  # Update tracker
                    except Exception as e:
                        print("❌ Error sending to Laravel:", e)
        else:
            time.sleep(0.1)  # Slightly more frequent loop for responsiveness

except KeyboardInterrupt:
    print("🔌 Script stopped by user.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("🔌 Serial port closed.")

        import serial

try:
    ser = serial.Serial('COM3', 9600, timeout=1)
    print("Port opened successfully")
    ser.close()
except Exception as e:
    print("Error:", e)
