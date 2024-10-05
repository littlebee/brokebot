import os
import subprocess
import log

ESPEAK_CMD = "espeak -v en+f5 -s 140"
ESPEAK_AFFIX = "--stdout | aplay"


def say(text):
    log.info(f"say: {text}")
    os.system(espeak_cmd(text))


def say_async(text):
    log.info(f"say_async: {text}")
    async_cmd(espeak_cmd(text))


def espeak_cmd(text):
    return f'{ESPEAK_CMD} "{text}" {ESPEAK_AFFIX}'


def async_cmd(cmd):
    subprocess.Popen(
        [cmd], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True
    )
