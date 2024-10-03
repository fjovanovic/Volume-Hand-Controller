import sys
import time

from termcolor import colored
import cv2

import utils


def main() -> None:
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cam.isOpened() == False:
        sys.exit(colored(
            'Camera could not be opened',
            'red'
        ))
    
    previous_time = time.time()

    while True:
        (success, img) = cam.read()
        if success == False:
            utils.error('Unable to process image', cam)
        
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

    cv2.destroyAllWindows()
    cam.release()


if __name__ == '__main__':
    main()