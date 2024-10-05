import sys
import time
from argparse import ArgumentParser

from termcolor import colored
import cv2

import utils


def main(no_landmarks: bool) -> None:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened() == False:
        sys.exit(colored(
            'Camera could not be opened',
            'red'
        ))
    
    previous_time = time.time()

    while True:
        (success, img) = cap.read()
        if success == False:
            utils.error('Unable to process image', cap)
        
        # Measure the FPS
        current_time = time.time()
        fps = int(1 / (current_time - previous_time))
        previous_time = current_time

        cv2.putText(
            img=img, 
            text=f'FPS: {fps}', 
            org=(10, 30), 
            fontFace=cv2.FONT_HERSHEY_COMPLEX, 
            fontScale=1, 
            color=(0, 255, 0), 
            thickness=1
        )

        cv2.imshow('Volume hand controller', img)
        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = ArgumentParser(
        usage='python3 main.py [-n | --no-landmarks]',
        description='Volume controller with hand',
        allow_abbrev=False
    )

    parser.add_argument(
        '-n', 
        '--no-landmarks', 
        dest='no_landmarks',
        action='store_true', 
        help='Disable landmarks'
    )
    args = parser.parse_args()
    
    main(no_landmarks=(args.no_landmarks == True))