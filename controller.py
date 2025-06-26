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
                time.sleep(0.05)  # Small delay for servo to reach position
                distances.append(sensor.get_distance())
            mind = min(distances)
            if mind < SAFE_DISTANCE:
                motors.stop()
                # --- Ask GPT what to do next ---
                prompt = (
                    f"I have an obstacle at {mind:.1f} cm in front of me. "
                    "Should I turn left, right, or wait? "
                    "Reply with one of: TURN_LEFT, TURN_RIGHT, WAIT."
                )
                cmd = gpt.ask_gpt(prompt)
                print("GPT suggests:", cmd)
                if "TURN_LEFT" in cmd:
                    # Example: turn left in place
                    motors.turn_left(DRIVE_SPEED)
                    time.sleep(0.5)
                    motors.stop()
                elif "TURN_RIGHT" in cmd:
                    motors.turn_right(DRIVE_SPEED)
                    time.sleep(0.5)
                    motors.stop()
                else:
                    time.sleep(1)
                # Resume driving forward
                motors.drive(DRIVE_SPEED)
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        motors.cleanup()
        sensor.cleanup()