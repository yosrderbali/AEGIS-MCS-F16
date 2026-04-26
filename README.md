# AEGIS MCS — F-16 Viper Mission Control System

![License](https://img.shields.io/badge/license-MIT-blue)
![Platform](https://img.shields.io/badge/platform-ESP32-green)
![Language](https://img.shields.io/badge/language-Arduino%20C%2B%2B%20%7C%20Python%20%7C%20HTML-orange)

## Description
AEGIS MCS is an open-source mission control system for the F-16 Viper fighter jet. It combines ESP32 sensors, Python bridge, and an AI-powered web dashboard (NEXUS-7) to provide real-time tactical situational awareness.

## Features
- Real-time pilot biometric monitoring (heart rate, G-force, fatigue)
- Interactive tactical radar with 5 zoom levels (50-500NM)
- NEXUS-7 AI — automatic threat analysis every 4 seconds
- Automatic mission replanning when threats detected
- Live sensor streaming via ESP32 WiFi
- Automatic pilot grounding alert at 75% fatigue

## Hardware
| Component | Role | Price |
|-----------|------|-------|
| ESP32 DevKit | Main controller + WiFi | ~$4 |
| DHT22 | Temperature & Humidity | ~$2 |
| BMP280 | Pressure & Altitude | ~$2 |
| MPU6050 | G-Force & Gyroscope | ~$3 |
| Breadboard + Wires | Connections | ~$3 |

**Total cost: ~$14**

## Software Stack
- **Arduino IDE** — ESP32 firmware
- **Python 3.15 + PySerial** — Serial bridge
- **HTML/CSS/JavaScript** — AEGIS Dashboard
- **Wokwi** — Circuit simulation

## How to Run
1. Upload `aegis_sensor_node_v3.ino` to ESP32
2. Install Python dependencies: `py -m pip install pyserial`
3. Run bridge: `py aegis_bridge.py`
4. Open `aegis_final.html` in Firefox
5. Connect to `LAUNCHPAD_OS` WiFi

## Project Structure
AEGIS-MCS-F16/
├── aegis_sensor_node_v3.ino   # ESP32 sensor code
├── aegis_bridge.py             # Python serial bridge
├── aegis_final.html            # AEGIS main dashboard
└── aegis_radar_ultimate.html   # Tactical radar

## Author
Yosr Derbali — Tunisia 🇹🇳

## License
MIT License
