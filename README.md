# Robot Car

Self-driving Raspberry Pi 5 car with obstacle avoidance.

## Structure

- `motors.py`: Motor control (drive, stop).
- `sensor.py`: Ultrasonic sensor + pan servo.
- `controller.py`: Main autonomous loop.
- `vision.py`: Optional camera-based detection.
- `chatgpt_client.py`: GPT integration.

## Installation

### 1. System Packages

```bash
sudo apt update
sudo apt install python3-pip python3-dev libatlas-base-dev libhdf5-dev python3-picamera2 -y
```

### 2. Project Setup

**(Recommended) Create and activate a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Python Packages

```bash
pip install -r requirements.txt
```

> **Note:**  
> - `picamera2` is installed via `apt` (see above), not pip.
> - If you use the camera, ensure your Raspberry Pi camera is enabled (`sudo raspi-config`).

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
  - ENA → GPIO12, IN1 → GPIO5, IN2 → GPIO6
  - ENB → GPIO13, IN3 → GPIO20, IN4 → GPIO21
- **Ultrasonic (HC-SR04)**:
  - TRIG → GPIO23, ECHO → GPIO24
- **Servo**:
  - SERVO_PIN → GPIO18
- **Camera**:
  - CSI ribbon to Pi camera port

## Dependency Summary

- Use `requirements.txt` for pip packages.
- Install `picamera2` with `apt`, not pip.
- Always activate your virtual environment before running or installing Python packages.

---

# Real Data Collecting

(Add your data collection instructions here.)