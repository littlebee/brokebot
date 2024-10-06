import cv2
import pygame
import threading

import log


class PlayStates(object):
    STOPPED = 0
    PLAYING = 1


class VideoFile(object):
    """
    Used to playback video (no audio support) of .mp4.

    This component does not self destruct.  When the video finishes playing,
    the last frame of the video is displayed until `.close()` is called
    """

    def __init__(self, surface, video_file, fps, on_playback_complete=None):
        self.surface = surface
        self.video_file = video_file
        self.fps = fps
        self.on_playback_complete = on_playback_complete

        self.has_closed = False

        self.play_state = PlayStates.STOPPED
        self.last_frame = None

        self.video_thread = None

        self.start_playback()

    def __del__(self):
        self.close()

    def start_playback(self):
        self.has_closed = False
        self.play_state = PlayStates.PLAYING
        log.info("video_file: creating video thread")
        self.video_thread = threading.Thread(target=self._video_thread)
        self.video_thread.start()

    def stop_playback(self):
        if self.play_state == PlayStates.PLAYING:
            self.play_state = PlayStates.STOPPED

    # needs to be called externally.  This component doesn't self destruct
    def close(self):
        if hasattr(self, "has_closed") and not self.has_closed:
            self.has_closed = True
            self.stop_playback()

    def render(self, t):
        if self.has_closed:
            return False

        if self.last_frame:
            self.surface.blit(self.last_frame, (0, 0))

        return True

    def _video_thread(self):

        log.info("video_file: _video_thread starting")
        video = cv2.VideoCapture(self.video_file)
        file_fps = video.get(cv2.CAP_PROP_FPS)
        clock = pygame.time.Clock()

        log.info(
            f"video_file: rendering frames file_fps={file_fps} self.fps={self.fps}"
        )

        while not self.has_closed and self.play_state == PlayStates.PLAYING:
            success, video_image = video.read()
            if not success:
                break
            self.last_frame = opencv_to_pyg(video_image)
            clock.tick(self.fps)

        log.info("video_thread: _video_thread stopping")
        video.release()

        self.video_thread = None
        self.play_state = PlayStates.STOPPED

        callable(self.on_playback_complete) and self.on_playback_complete()


def opencv_to_pyg(opencv_image):
    """
    Convert OpenCV images for Pygame.

    source: https://blanktar.jp/blog/2016/01/pygame-draw-opencv-image.html
    """
    # Since OpenCV is BGR and pygame is RGB, it is necessary to convert it.
    opencv_image = opencv_image[:, :, ::-1]
    # OpenCV(height,width,Number of colors), Pygame(width, height)So this is also converted.
    shape = opencv_image.shape[1::-1]
    pygame_image = pygame.image.frombuffer(opencv_image.tobytes(), shape, "RGB")

    return pygame_image
