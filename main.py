import sys
import time
import math
from argparse import ArgumentParser

from termcolor import colored
import cv2

import utils
from components import HandDetector, VolumeChanger


def main(reset_volume: bool) -> None:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened() == False:
        sys.exit(colored(
            'Camera could not be opened',
            'red'
        ))
    
    detector = HandDetector()
    volume = VolumeChanger(reset_volume)

    db = volume.get_initial_db()
    previous_time = time.time()

    while True:
        (success, img) = cap.read()
        if success == False:
            utils.error('Unable to process image', cap, volume)
        
        detector.draw_hands(img)
        lm_positions = detector.get_positions(img)

        # If hand is vissible then process hand landmarks
        if len(lm_positions) != 0:
            # Landmark 4: Thumb tip
            # Landmark 8: Index finger tip
            x1 = lm_positions[4][1]
            y1 = lm_positions[4][2]
            x2 = lm_positions[8][1]
            y2 = lm_positions[8][2]
            length = math.hypot(x2-x1, y2-y1)

            cv2.circle(
                img=img, 
                center=(x1, y1), 
                radius=10, 
                color=(255, 0, 255), 
                thickness=cv2.FILLED
            )
            cv2.circle(
                img=img, 
                center=(x2, y2), 
                radius=10, 
                color=(255, 0, 255), 
                thickness=cv2.FILLED
            )
            cv2.line(
                img=img, 
                pt1=(x1, y1), 
                pt2=(x2, y2), 
                color=(255, 0, 255), 
                thickness=1
            )

            db = volume.get_scaled_db(length)
            volume.set_volume(length)
        
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

        cv2.putText(
            img=img, 
            text=f'Volume: {db} dB', 
            org=(10, 60), 
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
    volume.reset_default_volume()


if __name__ == '__main__':
    parser = ArgumentParser(
        usage='python3 main.py [-r | --reset-volume]',
        description='Volume controller with hand',
        allow_abbrev=False
    )

    parser.add_argument(
        '-r', 
        '--reset-volume', 
        dest='reset_volume',
        action='store_true', 
        help='Restores the system volume to what it was ' \
            'before the script started'
    )
    args = parser.parse_args()
    
    main(reset_volume=args.reset_volume)