# 🌾 IoT Mobile App Controlled Agricultural Robot

> Final Year B.Tech Project — Electronics and Communication Engineering  
> College of Engineering Thalassery | APJ Abdul Kalam Technological University | 2025

---

## 📌 Overview

An IoT-based agricultural robot that automates essential farming operations — **irrigation, seed sowing, and pesticide spraying** — controlled wirelessly over Wi-Fi using MQTT. The system integrates real-time environmental sensing via a Raspberry Pi.

---

## ✨ Features

- 💧 **Automatic Irrigation** — soil moisture-driven pump activation
- 🌡️ **Environmental Sensing** — real-time temperature and humidity monitoring
- 🌱 **Seed Sowing** — servo-controlled seed dispensing mechanism
- 🧪 **Pesticide Spraying** — relay-triggered spray pump, manual or auto mode
- 📡 **MQTT Communication** — lightweight real-time data transfer

---

## 🛠️ Hardware Components

| Component | Model | Function |
|---|---|---|
| Microprocessor | Raspberry Pi 4 | Central controller, IoT communication |
| Soil Moisture Sensor | Capacitive type | Detects soil dryness for irrigation |
| Temp & Humidity Sensor | DHT11 | Environmental monitoring |
| Motor Driver | L293D | Controls DC motor direction and speed |
| DC Motors + Wheels | 6V–12V, 150–300 RPM | Robot locomotion |
| Relay Module | 2-channel, 5V | Switches water and pesticide pumps |
| Servo Motor | SG90 | Seed sowing and nozzle control |
| Power Supply | 12V Li-ion battery + LM7805 | Powers all modules |

---


## 📱 Mobile App *(Planned — Not Implemented)*

The mobile app was designed but not developed in this phase. The intended design (Flutter, Android/iOS) would have included:
- Live dashboard: soil moisture %, temperature °C, humidity %
- Manual control buttons: irrigation, spray, robot movement (F/B/L/R)
- Status indicators: pump ON/OFF, battery level
- Communication: MQTT over Wi-Fi (Mosquitto broker)

> Mobile app development is listed under Future Scope.

---

## 🔌 Circuit Overview

- **Power**: 12V battery → LM7805 → 5V for RPi and logic circuits
- **Motor Control**: L293D H-bridge — IN1–IN4 pins control direction; EN pins for PWM speed
- **Relay Driver**: NPN transistor (GPIO → base resistor → transistor → relay coil) + flyback diode
- **Sensors**: Soil moisture on GPIO 16, DHT11 on GPIO 13

---

## 💻 Software Stack

| Layer | Technology |
|---|---|
| Embedded (RPi) | Python 3 |

| IoT Protocol | MQTT (Mosquitto broker) |

---

## 📁 Project Structure

```
agri-robot/
├── src/
│   ├── main.py              # Main embedded code (Raspberry Pi)
│   ├── motor_control.py     # L293D motor driver functions
│   ├── sensor_reader.py     # DHT11 + soil moisture reading
│   └── relay_control.py     # Pump and spray relay control
├── docs/
│   └── report.pdf           # Full project report
├── images/
│   ├── circuit_diagram.jpg
│   ├── block_diagram.jpg
│   └── prototype.jpg
├── components.md
└── README.md
```

---

## 📊 Results

| Parameter | Result |
|---|---|
| Soil moisture accuracy | Correctly triggered irrigation below 35% |
| Temperature sensor accuracy | ±1°C |
| Wi-Fi range | Stable up to 20m |
| Control latency | < 1 second |
| Battery backup | ~90 minutes per charge |
| Pest detection confidence | > 0.5 threshold |

---

## 🚀 Future Scope

- Flutter mobile app for live sensor dashboard and manual robot control
- Camera-based pest detection using YOLOv8
- GPS-based autonomous field navigation
- Solar-powered battery charging
- Cloud dashboard with historical data analytics
- pH and nutrient sensors for precision agriculture

---

## 👥 Team

| Name | Roll No |
|---|---|
| Anudev S S | TLY22EC031 |
| Abhishek K | TLY22EC007 |
| Ajal Raj P P | TLY22EC020 |
| Fathima Henan | TLY22EC057 |

**Guide**: Ms. Anagha A, Assistant Professor, Dept. of ECE, College of Engineering Thalassery

---

## 📄 License

This project was developed for academic purposes under APJ Abdul Kalam Technological University.
