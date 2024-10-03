import sys

import cv2
from termcolor import colored


def error(message: str, cam: cv2.VideoCapture) -> None:
    cv2.destroyAllWindows()
    cam.release()
    sys.exit(colored(message, 'red'))