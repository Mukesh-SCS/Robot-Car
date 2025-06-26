import time
import motors
import sensor
import chatgpt_client as gpt

SAFE_DISTANCE = 20
PAN_ANGLES = [60, 90, 120]
DRIVE_SPEED = 70


def main():
    motors.setup()
    sensor.setup()
    try:
        print("Starting autonomous drive…")
        motors.drive(DRIVE_SPEED)
        while True:
            distances = []
            for ang in PAN_ANGLES:
                sensor.set_servo(ang)
                time.sleep(0.1)
                dist = sensor.get_distance()
                print(f"Angle {ang}: {dist:.1f} cm")
                distances.append(dist)

            mind = min(distances)
            if mind < SAFE_DISTANCE:
                print(f"Obstacle at {mind:.1f} cm detected. Stopping.")
                motors.stop()
                # Ask GPT for next action
                prompt = (
                    f"I have an obstacle at {mind:.1f} cm ahead. "
                    "Should I TURN_LEFT, TURN_RIGHT, or WAIT?"
                )
                cmd = gpt.ask_gpt(prompt).upper()
                print("GPT suggests:", cmd)
                if "TURN_LEFT" in cmd:
                    motors.turn_left(DRIVE_SPEED)
                elif "TURN_RIGHT" in cmd:
                    motors.turn_right(DRIVE_SPEED)
                else:
                    print("Waiting...")
                time.sleep(0.5)
                motors.stop()
                time.sleep(0.2)
                motors.drive(DRIVE_SPEED)

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        motors.cleanup()
        sensor.cleanup()


if __name__ == "__main__":
    main()