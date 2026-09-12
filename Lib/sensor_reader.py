# sensor_reader.py
# Reads DHT11 (temp + humidity) and soil moisture sensor (digital output)
# GPIO 13 -> DHT11 data pin
# GPIO 16 -> Soil moisture sensor D0 pin

import RPi.GPIO as GPIO
import Adafruit_DHT

# Pin Definitions
SOIL_PIN = 16  # D0 output of soil moisture sensor module
DHT_PIN = 13  # DHT11 data pin
DHT_SENSOR = Adafruit_DHT.DHT11


def setup_sensors():
    """Configure GPIO input pin for soil moisture sensor."""
    GPIO.setup(SOIL_PIN, GPIO.IN)
    print("[SENSOR] Sensors initialised.")


def read_soil_moisture():
    """
    Read digital output from soil moisture sensor module.

    The onboard comparator outputs:
    HIGH (1) -> soil is DRY -> irrigation needed
    LOW (0) -> soil is WET -> no irrigation needed

    Returns:
        bool: True = dry, False = wet
    """
    return GPIO.input(SOIL_PIN) == GPIO.HIGH


def read_dht11():
    """
    Read temperature and humidity from DHT11.
    Uses Adafruit_DHT which automatically retries on failure.

    Returns:
        tuple: (humidity: float, temperature: float)
        or (None, None) if read fails after retries
    """
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        return round(humidity, 1), round(temperature, 1)

    print("[SENSOR] DHT11 read failed.")
    return None, None


def read_all():
    """
    Read all sensors and return a single dictionary.

    Returns:
        dict: {
            'soil_dry': bool,
            'humidity': float or None,
            'temperature': float or None
        }
    """
    soil_dry = read_soil_moisture()
    humidity, temperature = read_dht11()

    return {
        'soil_dry': soil_dry,
        'humidity': humidity,
        'temperature': temperature
    }
