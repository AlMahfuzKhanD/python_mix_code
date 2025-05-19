import re
import serial
import time

PORT = 'COM3'
BAUD_RATE = 9600
TIMEOUT = 1

def extract_weights(data):
    """
    Extract weight strings from raw input like: '+000800211'
    Returns a list of weights as strings (e.g., ['800.211'])
    """
    # Match strings like +000800211 between STX () and ETX ()
    matches = re.findall(r'\x02([+-]\d{9})\x03', data)

    # Convert raw numbers to readable weights (optional decimal at 3 digits)
    readable = [f"{int(m)/1000:.3f}" for m in matches]
    return readable

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"✅ Connected to {PORT} at {BAUD_RATE} baud.")
    time.sleep(2)

    print("📡 Reading weight data... (Ctrl+C to stop)")

    while True:
        if ser.in_waiting:
            raw = ser.read(40)
            decoded = raw.decode('utf-8', errors='ignore')

            # Extract and print weights
            weights = extract_weights(decoded)
            for w in weights:
                print(f"⚖️ Weight: {w} kg")  # or g depending on your scale config
        else:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("🛑 Stopped by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("🔌 Serial connection closed.")