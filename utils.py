import sys

import cv2
from termcolor import colored


def error(message: str, cap: cv2.VideoCapture) -> None:
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(colored(message, 'red'))