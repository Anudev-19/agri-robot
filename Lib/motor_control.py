# motor_control.py
# Controls two DC motors through L293D H-bridge motor driver

# L293D wiring:
# Motor 1 (Left) -> IN1: GPIO17, IN2: GPIO27, EN1: GPIO12
# Motor 2 (Right) -> IN3: GPIO22, IN4: GPIO10, EN2: GPIO19

# EN1 / EN2 are driven with PWM to control speed.
# IN1-IN4 logic:
# IN1=HIGH, IN2=LOW -> Motor 1 forward
# IN1=LOW, IN2=HIGH -> Motor 1 backward
# (same logic for Motor 2 via IN3/IN4)

import RPi.GPIO as GPIO

# Pin Definitions
IN1 = 17
IN2 = 27
EN1 = 12  # Left motor
IN3 = 22
IN4 = 10
EN2 = 19  # Right motor

PWM_FREQ = 100  # Hz
DEFAULT_SPEED = 80  # duty cycle % (0-100)

_pwm1 = None
_pwm2 = None


def setup_motors():
    """Configure all motor driver GPIO pins and start PWM at 0 duty cycle."""
    global _pwm1, _pwm2

    for pin in (IN1, IN2, IN3, IN4, EN1, EN2):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    _pwm1 = GPIO.PWM(EN1, PWM_FREQ)
    _pwm2 = GPIO.PWM(EN2, PWM_FREQ)

    _pwm1.start(0)
    _pwm2.start(0)

    print("[MOTOR] L293D motor driver initialised.")


def _set_speed(speed: int = DEFAULT_SPEED):
    """Set PWM duty cycle for both enable pins to control speed."""
    _pwm1.ChangeDutyCycle(speed)
    _pwm2.ChangeDutyCycle(speed)


def move_forward(speed: int = DEFAULT_SPEED):
    """Drive both motors forward."""
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

    _set_speed(speed)
    print(f"[MOTOR] Forward (speed={speed}%)")


def move_backward(speed: int = DEFAULT_SPEED):
    """Drive both motors backward."""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

    _set_speed(speed)
    print(f"[MOTOR] Backward (speed={speed}%)")


def turn_left(speed: int = DEFAULT_SPEED):
    """
    Turn left: left motor backward, right motor forward.
    Robot pivots left on its own axis.
    """
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

    _set_speed(speed)
    print(f"[MOTOR] Turn Left (speed={speed}%)")


def turn_right(speed: int = DEFAULT_SPEED):
    """
    Turn right: left motor forward, right motor backward.
    Robot pivots right on its own axis.
    """
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

    _set_speed(speed)
    print(f"[MOTOR] Turn Right (speed={speed}%)")


def stop():
    """Stop both motors immediately."""
    for pin in (IN1, IN2, IN3, IN4):
        GPIO.output(pin, GPIO.LOW)

    _set_speed(0)
    print("[MOTOR] Stopped.")


def cleanup_motors():
    """Stop PWM signals on cleanup."""
    if _pwm1:
        _pwm1.stop()

    if _pwm2:
        _pwm2.stop()
