# relay_control.py
# Controls:
# - Water pump via Relay 1 (GPIO 23)
# - Pesticide pump via Relay 2 (GPIO 24)
# - SG90 Servo for seed sowing (GPIO 25, PWM)

# Relay module is ACTIVE-LOW:
# GPIO HIGH -> relay coil OFF -> pump OFF
# GPIO LOW -> relay coil ON -> pump ON

import RPi.GPIO as GPIO
import time

# Pin Definitions
WATER_PUMP_PIN = 23  # Relay 1 - irrigation
PESTICIDE_PUMP_PIN = 24  # Relay 2 - pesticide spray
SERVO_PIN = 25  # SG90 servo for seed sowing

# Active-LOW relay logic constants for readability
RELAY_ON = GPIO.LOW
RELAY_OFF = GPIO.HIGH

_servo_pwm = None


def setup_relays():
    """Initialise relay output pins (OFF by default) and servo PWM."""
    global _servo_pwm

    GPIO.setup(WATER_PUMP_PIN, GPIO.OUT)
    GPIO.setup(PESTICIDE_PUMP_PIN, GPIO.OUT)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    # Make sure both pumps are OFF at startup
    GPIO.output(WATER_PUMP_PIN, RELAY_OFF)
    GPIO.output(PESTICIDE_PUMP_PIN, RELAY_OFF)

    # Servo: 50Hz is standard for SG90
    _servo_pwm = GPIO.PWM(SERVO_PIN, 50)
    _servo_pwm.start(0)

    print("[RELAY] Relays and servo initialised (pumps OFF).")


# Water Pump (Irrigation)
def water_pump_on():
    GPIO.output(WATER_PUMP_PIN, RELAY_ON)
    print("[RELAY] Water pump ON.")


def water_pump_off():
    GPIO.output(WATER_PUMP_PIN, RELAY_OFF)
    print("[RELAY] Water pump OFF.")


def irrigate(duration_sec: float = 5.0):
    """
    Run irrigation pump for a fixed duration.
    After duration_sec seconds, pump switches OFF automatically.
    """
    water_pump_on()
    time.sleep(duration_sec)
    water_pump_off()
    print(f"[RELAY] Irrigation complete - ran for {duration_sec}s.")


# Pesticide Pump (Spray)
def pesticide_pump_on():
    GPIO.output(PESTICIDE_PUMP_PIN, RELAY_ON)
    print("[RELAY] Pesticide pump ON.")


def pesticide_pump_off():
    GPIO.output(PESTICIDE_PUMP_PIN, RELAY_OFF)
    print("[RELAY] Pesticide pump OFF.")


def spray_pesticide(duration_sec: float = 3.0):
    """Run pesticide spray pump for a fixed duration."""
    pesticide_pump_on()
    time.sleep(duration_sec)
    pesticide_pump_off()
    print(f"[RELAY] Spray complete - ran for {duration_sec}s.")


# Servo Motor (Seed Sowing)
def _angle_to_duty(angle: int) -> float:
    """
    Convert servo angle (0-180 degrees) to SG90 duty cycle.

    SG90 spec:
    0 degrees -> 1ms pulse -> 2.5% duty @ 50Hz
    180 degrees -> 2ms pulse -> 12.5% duty @ 50Hz
    """
    return 2.5 + (angle / 180.0) * 10.0


def servo_set_angle(angle: int):
    """Move servo to specified angle (0-180 degrees) and hold briefly."""
    duty = _angle_to_duty(angle)
    _servo_pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    _servo_pwm.ChangeDutyCycle(0)  # set to 0 to stop jitter after reaching angle


def sow_seed():
    """
    Dispense one seed:
    1. Rotate gate servo to 90 degrees -> seed gate opens -> seed falls
    2. Wait 1 second for seed to drop
    3. Return servo to 0 degrees -> gate closes
    """
    print("[SERVO] Sowing seed...")
    servo_set_angle(90)  # open gate
    time.sleep(1.0)  # let seed fall through
    servo_set_angle(0)  # close gate
    print("[SERVO] Seed dispensed.")


def cleanup_relays():
    """Turn off all pumps and stop servo PWM before GPIO cleanup."""
    water_pump_off()
    pesticide_pump_off()

    if _servo_pwm:
        _servo_pwm.stop()
