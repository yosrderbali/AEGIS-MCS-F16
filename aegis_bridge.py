# ============================================
#   AEGIS BRIDGE v1.0
#   Reads Arduino sensor data via Serial
#   Serves it to AEGIS dashboard via HTTP
# ============================================

import serial
import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# ── CONFIG ──────────────────────────────────
SERIAL_PORT = 'COM3'       # Change to your Arduino port (COM3, COM4 etc on Windows)
BAUD_RATE   = 9600
SERVER_PORT = 5000
# ────────────────────────────────────────────

# Latest sensor data (shared between threads)
sensor_data = {
    "temp":       24.0,
    "humidity":   58.0,
    "pressure":   1013.25,
    "altitude":   0.0,
    "gForce":     1.0,
    "gX":         0.0,
    "gY":         0.0,
    "gZ":         1.0,
    "gyroX":      0.0,
    "gyroY":      0.0,
    "gyroZ":      0.0,
    "battery":    94.0,
    "maxG":       1.0,
    "flightMins": 0,
    "flightSecs": 0,
    "connected":  False
}

# ── HTTP SERVER ──────────────────────────────
class AEGISHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Allow AEGIS dashboard to fetch data
        if self.path == '/sensors':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow browser access
            self.end_headers()
            self.wfile.write(json.dumps(sensor_data).encode())

        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            status = {"connected": sensor_data["connected"], "port": SERIAL_PORT}
            self.wfile.write(json.dumps(status).encode())

        else:
            self.send_response(404)
            self.end_headers()

    # Silence server logs
    def log_message(self, format, *args):
        pass

# ── SERIAL READER ────────────────────────────
def read_arduino():
    global sensor_data

    print(f"[AEGIS] Connecting to Arduino on {SERIAL_PORT}...")

    while True:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
            print(f"[AEGIS] ✓ Arduino connected on {SERIAL_PORT}")
            sensor_data["connected"] = True

            buffer = ""

            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()

                if line == '{':
                    buffer = '{'
                elif line == '}':
                    buffer += '}'
                    try:
                        parsed = json.loads(buffer)
                        sensor_data.update(parsed)
                        sensor_data["connected"] = True
                        print(f"[SENSOR] T:{parsed.get('temp')}°C | G:{parsed.get('gForce')}G | B:{parsed.get('battery')}%")
                    except json.JSONDecodeError:
                        pass
                    buffer = ""
                elif buffer:
                    # Remove trailing comma for valid JSON
                    clean = line.rstrip(',')
                    buffer += clean

        except serial.SerialException as e:
            print(f"[AEGIS] ✗ Arduino disconnected: {e}")
            sensor_data["connected"] = False
            print("[AEGIS] Retrying in 3 seconds...")
            time.sleep(3)

        except Exception as e:
            print(f"[AEGIS] Error: {e}")
            time.sleep(3)

# ── MAIN ─────────────────────────────────────
if __name__ == '__main__':
    print("============================================")
    print("   AEGIS BRIDGE v1.0                       ")
    print("   Arduino → Python → AEGIS Dashboard      ")
    print("============================================")

    # Start serial reader in background thread
    serial_thread = threading.Thread(target=read_arduino, daemon=True)
    serial_thread.start()

    # Start HTTP server
    print(f"[AEGIS] Starting server on http://localhost:{SERVER_PORT}")
    print(f"[AEGIS] Dashboard fetches from: http://localhost:{SERVER_PORT}/sensors")
    print(f"[AEGIS] Press Ctrl+C to stop")
    print("--------------------------------------------")

    try:
        server = HTTPServer(('localhost', SERVER_PORT), AEGISHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[AEGIS] Bridge stopped.")
