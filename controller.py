# controller.py
import time
import motors
import sensor

# Configuration parameters
SAFE_DISTANCE = 20       # cm
PAN_ANGLES = [60, 90, 120]  # degrees for sweeping
DRIVE_SPEED = 70         # percentage PWM


def main():
    """
    Main loop: drive forward and stop on obstacle detection.
    """
    motors.setup()
    sensor.setup()
    try:
        print("Starting autonomous drive...")
        motors.drive(DRIVE_SPEED)
        while True:
            # Sweep ultrasonic sensor and collect distances
            distances = []
            for angle in PAN_ANGLES:
                sensor.set_servo(angle)
                d = sensor.get_distance()
                distances.append(d)
            min_dist = min(distances)
            print(f"Distances: {', '.join(f'{d:.1f}' for d in distances)} cm")

            if min_dist < SAFE_DISTANCE:
                print("Obstacle detected! Stopping.")
                motors.stop()
                # Wait until clear at center angle
                while True:
                    sensor.set_servo(90)
                    if sensor.get_distance() > SAFE_DISTANCE:
                        break
                    time.sleep(0.1)
                print("Path clear. Resuming.")
                motors.drive(DRIVE_SPEED)

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting...")
    finally:
        motors.cleanup()
        sensor.cleanup()


if __name__ == "__main__":
    main()   
      