#!/usr/bin/env python3
import cv2
from pygame.locals import (
    KEYDOWN,
    K_q,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    FINGERDOWN,
    FINGERUP,
)

import pygame
import sys
import time
import os

from video_file import VideoFile
import log

RENDER_FPS = 15

pygame.init()
pygame.display.set_caption("Join the love frame")
screen = pygame.display.set_mode([600, 1024], pygame.NOFRAME)

DISPLAY_VIDEO_FILE = "media/brokebot display.mp4"


class VideoPlayer(object):

    def __init__(self):
        # ## Using a pygame Surface causes video lag :(
        # self.surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.surface = screen

        self.clock = pygame.time.Clock()
        self.last_mousedown_pos = None
        self.video_file = VideoFile(
            self.surface, DISPLAY_VIDEO_FILE, RENDER_FPS, self.handle_video_end
        )

    def handle_video_end(self):
        # endless loop
        log.info("handle_video_end")
        self.video_file.start_playback()

    def render_loop(self):
        try:
            while True:
                for event in pygame.event.get():
                    # print(f"got event from pygame {event}")
                    isQuitKey = event.type == KEYDOWN and event.key == K_q
                    if event.type == pygame.QUIT or isQuitKey:
                        sys.exit(0)
                        break

                    translated_event = self.translate_touch_event(event)

                    if self._is_quit_gesture(translated_event):
                        log.info(
                            f"got quit gesture {self.last_mousedown_pos}, {translated_event}"
                        )
                        # sys.exit(0)
                        os.system("reboot")
                        break

                self.surface.fill((0, 0, 0))

                # the current timestamp is passed so that animated components can
                # have a reliable time sequence when running on slower SBCs like
                # the raspberry pi4
                self.video_file.render(time.time())

                # using a surface here increased live video lag
                # screen.blit(self.surface, (0, 0))

                pygame.display.update()
                self.clock.tick(RENDER_FPS)

        except (KeyboardInterrupt, SystemExit):
            pygame.quit()
            cv2.destroyAllWindows()

    # This is a secret (shhhhh) gesture to exit the love-frame app to the
    # Raspian desktop.  Like so you can configure the network.
    #
    # Swiping from the bottom of the screen to the top will cause this function
    # to return True
    def _is_quit_gesture(self, translated_event):
        l_pos = self.last_mousedown_pos
        if translated_event.type == MOUSEBUTTONDOWN:
            c_pos = translated_event.pos
            # print(f"is_quit_gesture: mousedown {c_pos[0]} {time.time()} {translated_event}")
            self.last_mousedown_pos = c_pos
            return False
        elif translated_event.type == MOUSEBUTTONUP:
            c_pos = translated_event.pos
            # print(f"is_quit_gesture: mouseup {c_pos[0]} {time.time()} {translated_event}")
            return l_pos and l_pos[1] > 500 and c_pos[1] < 100

        return False

    def translate_touch_event(self, event):
        """
        If event is FINGERDOWN, this function returns a MOUSEBUTTONDOWN
        event with a `pos` member that is translated from the FINGERDOWN x and y

        Other events are returned untouched
        """
        event_out = event
        if event.type == FINGERDOWN or event.type == FINGERUP:
            w, h = self.surface.get_size()
            pos = (int(event.x * w), int(event.y * h))
            # print(f"got touch event {event.x},{event.y} {w},{h} -> {pos}")
            event_type = MOUSEBUTTONDOWN if event.type == FINGERDOWN else MOUSEBUTTONUP
            event_out = pygame.event.Event(event_type, pos=pos)

        return event_out


if __name__ == "__main__":
    app = VideoPlayer()
    app.render_loop()
