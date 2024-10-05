#!/usr/bin/env python3

import log
import time

from servo import Servo, DEFAULT_STEP_DELAY

# index in Head.servos
PAN_SERVO = 0
TILT_SERVO = 1

PAN_CHANNEL = 14
TILT_CHANNEL = 15

PAN_MIN = 40
PAN_CENTER = 90
PAN_MAX = 160

TILT_MIN = 30
TILT_CENTER = 60
TILT_MAX = 90


class Head:
    servos = [
        Servo(PAN_CHANNEL, PAN_MIN, PAN_MAX),
        Servo(TILT_CHANNEL, TILT_MIN, TILT_MAX),
    ]

    def __init__(self):
        pass

    def pause(self):
        Head.pause_event.clear()

    def resume(self):
        Head.pause_event.set()

    def center_head(self):
        self.pan_to(PAN_CENTER)
        self.tilt_to(TILT_CENTER)

    def pan(self, relativeDegrees, wait=False):
        servo = Head.servos[PAN_SERVO]
        servo.move_to(servo.current_angle + relativeDegrees)
        if wait:
            servo.wait_for_motor_stopped()

    def pan_to(self, angle, wait=False):
        servo = Head.servos[PAN_SERVO]
        servo.move_to(angle)
        if wait:
            servo.wait_for_motor_stopped()

    def tilt(self, relativeDegrees, wait=False):
        servo = Head.servos[TILT_SERVO]
        servo.move_to(servo.current_angle + relativeDegrees)
        if wait:
            servo.wait_for_motor_stopped()

    def tilt_to(self, angle, wait=False):
        servo = Head.servos[TILT_SERVO]
        servo.move_to(angle)
        if wait:
            servo.wait_for_motor_stopped()

    def wait_for_all_stopped(self):
        for servo in Head.servos:
            servo.wait_for_motor_stopped()

    def bang_your_head(self):
        pan = Head.servos[PAN_SERVO]
        tilt = Head.servos[TILT_SERVO]
        log.info("bang_your_head")

        # reset both, but do tilt first to not swing into wall
        # when when panning
        tilt.move_to(70)
        tilt.wait_for_motor_stopped()
        pan.move_to(PAN_CENTER)
        pan.wait_for_motor_stopped()

        pan.step_delay = DEFAULT_STEP_DELAY
        for i in range(3):
            tilt.step_delay = DEFAULT_STEP_DELAY
            tilt.move_to(TILT_MIN)
            tilt.wait_for_motor_stopped()
            tilt.step_delay = DEFAULT_STEP_DELAY / 10
            tilt.move_to(TILT_MAX)
            tilt.wait_for_motor_stopped()
            time.sleep(1)

        tilt.step_delay = DEFAULT_STEP_DELAY

    def look_to_sky(self):
        pan = Head.servos[PAN_SERVO]
        tilt = Head.servos[TILT_SERVO]
        log.info("look_to_sky")

        pan.move_to(PAN_CENTER)
        tilt.move_to(TILT_MIN)

    def look_to_sky_left(self):
        pan = Head.servos[PAN_SERVO]
        tilt = Head.servos[TILT_SERVO]
        log.info("look_to_sky_left")

        tilt.move_to(TILT_CENTER)
        tilt.wait_for_motor_stopped()

        pan.move_to(PAN_MIN)
        tilt.move_to(TILT_MIN)

    def look_to_sky_right(self):
        pan = Head.servos[PAN_SERVO]
        tilt = Head.servos[TILT_SERVO]
        log.info("look_to_sky_right")

        tilt.move_to(TILT_CENTER)
        tilt.wait_for_motor_stopped()

        pan.move_to(PAN_MAX)
        tilt.move_to(TILT_MIN)

    def look_over_shoulder_left(self):
        pan = Head.servos[PAN_SERVO]
        tilt = Head.servos[TILT_SERVO]
        log.info("look_over_shoulder_left")

        tilt.move_to(TILT_CENTER)
        tilt.wait_for_motor_stopped()

        pan.move_to(PAN_MIN)
        tilt.move_to(TILT_MAX)

    def look_over_shoulder_right(self):
        pan = Head.servos[PAN_SERVO]
        tilt = Head.servos[TILT_SERVO]
        log.info("look_over_shoulder_right")

        tilt.move_to(TILT_CENTER)
        tilt.wait_for_motor_stopped()

        pan.move_to(PAN_MAX)
        tilt.move_to(TILT_MAX)


if __name__ == "__main__":
    head = Head()

    sequence = [
        head.bang_your_head,
        head.look_to_sky,
        head.bang_your_head,
        head.look_to_sky_left,
        head.bang_your_head,
        head.look_to_sky_right,
    ]

    try:
        while True:
            for seq in sequence:
                seq()
                time.sleep(5)
                head.wait_for_all_stopped()

    except KeyboardInterrupt:
        head.stop_thread()

        head = Head()
        head.center_head()
        head.stop_thread()
