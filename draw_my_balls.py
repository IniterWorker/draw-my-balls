import os
import cv2
import argparse
import sys
from collections import deque

from cfinderCV import CircleFinderFactory
from cfinderCV import Circle


def draw_circle(image, circle: Circle):
    # draw the outer circle
    cv2.circle(image, (circle.x, circle.y), circle.radius, (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(image, (circle.x, circle.y), 2, (0, 0, 255), 3)


def draw_line(image, circle_a: Circle, circle_b: Circle, thickness: int):
    cv2.line(image, (circle_a.x, circle_a.y), (circle_b.x, circle_b.y), (255, 0, 0), thickness)


def draw_deque_circles(image, cache: deque):
    init = False
    circle_tmp = None
    for circle in cache:
        if init is False:
            init = True
            circle_tmp = circle
        else:
            draw_line(image, circle, circle_tmp, circle.radius)
            circle_tmp = circle
        # draw circle over
        draw_circle(image, circle)


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def use_video(args, pts):
    circle_finder = CircleFinderFactory.create(args["algorithm"])

    try:
        device = int(args["video"])
        camera = cv2.VideoCapture(device)
    except:
        print("Video Capture on device")
        camera = cv2.VideoCapture(args["video"])

    # first init params
    circle_finder.init_params(args)

    if not camera.isOpened():
        print("Video Capture Failed")
    else:
        print("Video Capture Started")
        print("Press Q to quit")
        while True:
            # grab the current frame
            (grabbed, frame) = camera.read()

            if args.get("video") and not grabbed:
                break

            # run finder algorithm
            processing, circle = circle_finder.compute(frame)

            # store circle
            if circle.x > -1:
                pts.appendleft(circle)

            # drawing deque
            draw_deque_circles(frame, pts)

            # TODO : remove the if processing is None (compute time optimization)
            cv2.imshow("Compute Video", frame if args["processing"] is False or processing is None else processing)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("b"):
                circle_finder = CircleFinderFactory.create("Basic")
                circle_finder.init_params(args)

            if key == ord("t"):
                circle_finder = CircleFinderFactory.create("Tracking")
                circle_finder.init_params(args)

            if key == ord("c"):
                circle_finder = CircleFinderFactory.create("Colour")
                circle_finder.init_params(args)

            # if the 'q' key is pressed, stop the loop

            if key == ord("q"):
                break

        camera.release()
    cv2.destroyAllWindows()


def use_image(args, pts):
    circle_finder = CircleFinderFactory.create(args["algorithm"])

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), args["image"])
    image = cv2.imread(path)

    # run finder algorithm
    circle_finder.init_params(args)
    processing, circle = circle_finder.compute(image)

    # store circle
    pts.appendleft(circle)

    # drawing deque
    draw_deque_circles(image, pts)

    cv2.imshow("Compute Image", image if args["processing"] is False else processing)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print("OpenCV version: " + cv2.__version__)

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help="Path to the image source")
    ap.add_argument("-b", "--buffer", type=int, default=64, help="Buffer size of vertex")
    ap.add_argument("-v", "--video", help="Path to the video source (device/filename)", default=1)
    ap.add_argument("-a", "--algorithm", help="Select algorithm: " + str(CircleFinderFactory.list()), default="basic")
    ap.add_argument("-l", "--lower", type=int, nargs=3, help="Custom palette lower (default=\"29 86 6\")",
                    default=[23, 86, 122])
    ap.add_argument("-u", "--upper", type=int, nargs=3, help="Custom palette lower (default=\"64 255 255\")",
                    default=[90, 255, 255])
    ap.add_argument("-p", "--processing", type=str2bool, nargs='?',
                    const=True, default=False, help="Display processing render")

    args = vars(ap.parse_args())

    # configure deque maximum len
    pts = deque(maxlen=int(args["buffer"]))

    if args.get("image", False):
        use_image(args, pts)
    elif args.get("video", False):
        use_video(args, pts)
    else:
        sys.stderr.write("Choose between image or video. (--help)\n")
        sys.exit(1)
