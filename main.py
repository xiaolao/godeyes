# coding: utf-8
import mxnet as mx
from mtcnn_detector import MtcnnDetector
import cv2

import os
import time

# import datetime
# starttime = datetime.datetime.now()
from utils.gen_loc import box_to_location, fillter_outlier

detector = MtcnnDetector(model_folder='model', ctx=mx.cpu(0), num_worker = 4 , accurate_landmark = False)

img = cv2.imread('2019MSEtest.jpeg')

# run detector
results = detector.detect_face(img)

if results is not None:
    total_boxes = fillter_outlier(results[0])
    points = results[1]

    # print(total_boxes)
    # extract aligned face chips
    chips = detector.extract_image_chips(img, points, 144, 0.37)
    # for i, chip in enumerate(chips):
    #     cv2.imshow('chip_'+str(i), chip)
    #     cv2.imwrite('chip_'+str(i)+'.png', chip)

    draw = img.copy()
    for b in total_boxes:
        cv2.rectangle(draw, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (255, 0, 255), thickness=1)

    # for p in points:
    #     for i in range(5):
    #         cv2.circle(draw, (p[i], p[i + 5]), 1, (0, 0, 255), 2)

    # w, h = img.shape[0:2]
    # draw = cv2.resize(draw, (int(h / 3), int(w / 3)))

    # print("Time used:", (datetime.datetime.now() - starttime))
    box_to_location(total_boxes)
    cv2.imshow("detection result", draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# --------------
# test on camera
# --------------
'''
camera = cv2.VideoCapture(0)
while True:
    grab, frame = camera.read()
    img = cv2.resize(frame, (320,180))

    t1 = time.time()
    results = detector.detect_face(img)
    print 'time: ',time.time() - t1

    if results is None:
        continue

    total_boxes = results[0]
    points = results[1]

    draw = img.copy()
    for b in total_boxes:
        cv2.rectangle(draw, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (255, 255, 255))

    for p in points:
        for i in range(5):
            cv2.circle(draw, (p[i], p[i + 5]), 1, (255, 0, 0), 2)
    cv2.imshow("detection result", draw)
    cv2.waitKey(30)
'''