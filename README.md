# Robot Car

Self-driving Raspberry Pi 5 car with obstacle avoidance.

## Structure

- `motors.py`: Motor control (drive, stop).
- `sensor.py`: Ultrasonic sensor + pan servo.
- `controller.py`: Main autonomous loop.
- `vision.py`: Optional camera-based detection.

## Installation

```bash
sudo apt update && sudo apt install python3-pip python3-dev libatlas-base-dev libhdf5-dev -y
pip3 install -r requirements.txt
```

## Usage

```bash
python3 controller.py
```

Optionally:
```bash
python3 vision.py
```

## Wiring

- **Motors (L298N)**:
  - ENA→GPIO12, IN1→GPIO5, IN2→GPIO6
  - ENB→GPIO13, IN3→GPIO20, IN4→GPIO21
- **Ultrasonic (HC-SR04)**:
  - TRIG→GPIO23, ECHO→GPIO24
- **Servo**:
  - SERVO_PIN→GPIO18
- **Camera**:
  - CSI ribbon to Pi camera port



# Real Data Collecting.