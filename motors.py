import RPi.GPIO as GPIO

# Motor pin definitions
ENA = 12  # PWM pin for left motor
IN1 = 5   # Direction pin 1 for left motor
IN2 = 6   # Direction pin 2 for left motor
ENB = 13  # PWM pin for right motor
IN3 = 20  # Direction pin 1 for right motor
IN4 = 21  # Direction pin 2 for right motor

# PWM frequency (Hz)
FREQ = 1000

# PWM objects
pwm_left = None
pwm_right = None

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((IN1, IN2, IN3, IN4), GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup((ENA, ENB), GPIO.OUT)
    global pwm_left, pwm_right
    pwm_left = GPIO.PWM(ENA, FREQ)
    pwm_right = GPIO.PWM(ENB, FREQ)
    pwm_left.start(0)
    pwm_right.start(0)


def drive(speed: int = 50):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)


def turn_left(speed: int = 50):
    # Pivot left
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)


def turn_right(speed: int = 50):
    # Pivot right
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)


def stop():
    if pwm_left:
        pwm_left.ChangeDutyCycle(0)
    if pwm_right:
        pwm_right.ChangeDutyCycle(0)


def cleanup():
    if pwm_left:
        pwm_left.stop()
    if pwm_right:
        pwm_right.stop()
    GPIO.cleanup()