import sys

from termcolor import colored
import cv2


def main() -> None:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened() == False:
        sys.exit(colored(
            'Camera could not be opened',
            'red'
        ))

    while True:
        (success, img) = cap.read()

        cv2.imshow('Volume hand controller', img)
        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    main()