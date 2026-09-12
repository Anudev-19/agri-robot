# main.py
# IoT Mobile App Controlled Agricultural Robot
# College of Engineering Thalassery — Final Year Project 2025
#
# Runs on Raspberry Pi 4.
# Performs automatic irrigation based on soil moisture,
# accepts manual commands via MQTT, and continuously
# publishes sensor data to the MQTT broker.
#
# MQTT Topics:
#   Publish  → "agribot/sensors"   (sensor readings)
#   Subscribe → "agribot/commands"  (control commands)
#
# Valid commands (sent as plain strings):
#   Movement  : FORWARD | BACKWARD | LEFT | RIGHT | STOP
#   Actuators : IRRIGATE | SPRAY | SOW

import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

import sensor_reader
import motor_control
import relay_control

# ── GPIO Global Mode ─────────────────────────────────────────────────────────────
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# ── Configuration ────────────────────────────────────────────────────────────────
MQTT_BROKER          = "localhost"          # Mosquitto broker running on the same RPi
MQTT_PORT            = 1883
MQTT_TOPIC_SENSORS   = "agribot/sensors"   # publish sensor data
MQTT_TOPIC_COMMANDS  = "agribot/commands"  # receive control commands

SENSOR_POLL_INTERVAL = 5    # seconds between each sensor read cycle

# ── MQTT: Connection Callback ────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Connected to broker ({MQTT_BROKER}:{MQTT_PORT})")
        client.subscribe(MQTT_TOPIC_COMMANDS)
        print(f"[MQTT] Subscribed to '{MQTT_TOPIC_COMMANDS}'")
    else:
        print(f"[MQTT] Connection failed — return code: {rc}")

# ── MQTT: Message Callback ───────────────────────────────────────────────────────
def on_message(client, userdata, msg):
    """
    Decode incoming MQTT command and trigger the corresponding action.
    MQTT runs in a background thread, so this executes concurrently
    with the sensor loop in the main thread.
    """
    command = msg.payload.decode("utf-8").strip().upper()
    print(f"[MQTT] Command received: '{command}'")

    command_map = {
        "FORWARD"  : motor_control.move_forward,
        "BACKWARD" : motor_control.move_backward,
        "LEFT"     : motor_control.turn_left,
        "RIGHT"    : motor_control.turn_right,
        "STOP"     : motor_control.stop,
        "IRRIGATE" : relay_control.irrigate,
        "SPRAY"    : relay_control.spray_pesticide,
        "SOW"      : relay_control.sow_seed,
    }

    action = command_map.get(command)
    if action:
        action()
    else:
        print(f"[MQTT] Unknown command: '{command}'. Ignored.")

# ── Hardware Initialisation ──────────────────────────────────────────────────────
def initialise_hardware():
    sensor_reader.setup_sensors()
    motor_control.setup_motors()
    relay_control.setup_relays()
    print("[INIT] All hardware modules ready.")
    print("-" * 50)

# ── Sensor Loop ──────────────────────────────────────────────────────────────────
def sensor_loop(mqtt_client):
    """
    Main control loop:
      1. Read all sensors every SENSOR_POLL_INTERVAL seconds
      2. Auto-irrigate if soil is dry
      3. Publish sensor data to MQTT broker
    """
    print("[MAIN] Sensor loop started.")

    while True:
        data        = sensor_reader.read_all()
        soil_dry    = data['soil_dry']
        humidity    = data['humidity']
        temperature = data['temperature']

        print(f"[SENSOR] Soil Dry: {soil_dry} | Temp: {temperature}°C | Humidity: {humidity}%")

        # ── Automatic Irrigation ─────────────────────────────────────────────────
        if soil_dry:
            print("[AUTO] Soil is dry → starting auto-irrigation.")
            relay_control.irrigate(duration_sec=5.0)

        # ── Publish to MQTT ──────────────────────────────────────────────────────
        if mqtt_client and humidity is not None and temperature is not None:
            payload = (
                f"soil_dry={int(soil_dry)},"
                f"temperature={temperature},"
                f"humidity={humidity}"
            )
            mqtt_client.publish(MQTT_TOPIC_SENSORS, payload)
            print(f"[MQTT] Published → {payload}")

        time.sleep(SENSOR_POLL_INTERVAL)

# ── Entry Point ──────────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  AgroBot — IoT Agricultural Robot")
    print("  College of Engineering Thalassery, 2025")
    print("=" * 50)

    initialise_hardware()

    # ── Set Up MQTT Client ───────────────────────────────────────────────────────
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        mqtt_client.loop_start()   # MQTT runs in a background thread
    except Exception as e:
        print(f"[MQTT] Could not connect to broker: {e}")
        print("[MQTT] Continuing in standalone mode (no MQTT).")
        mqtt_client = None

    # ── Run Main Loop ────────────────────────────────────────────────────────────
    try:
        sensor_loop(mqtt_client)

    except KeyboardInterrupt:
        print("\n[MAIN] Keyboard interrupt received — shutting down.")

    finally:
        print("[MAIN] Running cleanup...")
        motor_control.stop()
        relay_control.cleanup_relays()
        motor_control.cleanup_motors()
        if mqtt_client:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
        GPIO.cleanup()
        print("[MAIN] Cleanup complete. Goodbye.")

if __name__ == "__main__":
    main()
