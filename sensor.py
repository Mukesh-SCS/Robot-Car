# sensor.py

import RPi.GPIO as GPIO
import time

# Ultrasonic sensor pins\NTRIG = 23  # Trigger pin
ECHO = 24  # Echo pin

# Servo pin\SERVO_PIN = 18\N
# Servo PWM frequency
FREQ = 50

def setup():
    """
    Initialize GPIO for ultrasonic sensor and servo.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    global servo
    servo = GPIO.PWM(SERVO_PIN, FREQ)
    servo.start(0)
    time.sleep(0.5)  # allow servo to initialize


def set_servo(angle: float):
    """
    Move servo to specified angle (0-180°).
    """
    duty = 2 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.2)
    servo.ChangeDutyCycle(0)


def get_distance() -> float:
    """
    Trigger ultrasonic pulse and measure distance in cm.
    """
    # Send trigger pulse
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)
    
    # Measure echo pulse duration
    start = time.time()
    timeout = start + 0.04
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        start = time.time()
    stop = time.time()
    timeout = stop + 0.04
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        stop = time.time()
    
    # Calculate distance
    duration = stop - start
    distance = (duration * 34300) / 2  # speed of sound = 34300 cm/s
    return max(0.0, distance)


def cleanup():
    """
    Stop servo PWM and clean up GPIO.
    """
    if 'servo' in globals():
        servo.stop()
    GPIO.cleanup()