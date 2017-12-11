import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import operator


def load_videos():
    video = []
    for root, dir, files in os.walk('.'):
        for file in files:
            if file.endswith('.avi'):
                print(root+file)
                video.append(root+'/'+file)
    return video


def getROItrack(frame):
    h, w = frame.shape[:2]
    return frame[int(h/1.8):, 15:-120]


def save_frame(cap, number=323, filename='pociag5.jpg'):
    cap.set(cv2.CAP_PROP_POS_FRAMES, number)
    ret, frame = cap.read()
    cv2.imwrite(filename, frame)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


def search_track(frame):
    roi = getROItrack(frame)
    roi = cv2.blur(roi[:, :, 2], (5, 5))

    ret, thres = cv2.threshold(roi, 100, 255, 0)
    thres = cv2.dilate(thres, (25, 25))
    thres = cv2.erode(thres, (25, 25))

    _, contours, hierarchy = cv2.findContours(thres, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    return frame

last_train_key = 'track'
def search_train(frame):
    global last_train_key
    p1, p2 = (210, 250), (300, 400)
    cv2.rectangle(frame, p1, p2, (100, 200, 50), thickness=4)
    roi = frame[250:400, 210:300]
    hist, bins = np.histogram(roi.ravel(), 16, [0, 255])
    values = dict((k, float('inf')) for k in temp.keys())
    for key in temp.keys():
        for i in range(len(temp[key])):
            dist = np.linalg.norm(hist - temp[key][i])
            values[key] = min(values[key], dist)
    values[last_train_key] *= 0.9  # histereza
    factor = 1.0 / sum(values.values())
    normalised_d = {k: (1-v * factor) for k, v in values.items()}
    print(normalised_d)
    result = max(normalised_d, key=normalised_d.get)
    last_train_key = result
    return result


def run_movie(num):
    #video = load_videos()
    #cap = cv2.VideoCapture(video[num])
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    frame = getROItrack(frame)
    h, w = frame.shape[:2]
    box_size = int(w/5)
    os = int(w/2) - int(box_size/1.5)
    box = {'left': ((os-box_size, h), (os, h-box_size)),
           'center': ((int(os-box_size/2), h), (int(os+box_size/2), h-box_size)),
            'right': ((os, h), (os+box_size, h-box_size))}
    while True:
        ret, frame = cap.read()
        if ret != True:
            break

        train = search_train(frame)
        #res = search_track(frame)
        cv2.putText(frame, str(int(cap.get(cv2.CAP_PROP_POS_FRAMES))), (50,50), cv2.FONT_HERSHEY_PLAIN, 5.0, (150, 200, 0), 5)
        cv2.putText(frame, train, (50,100), cv2.FONT_HERSHEY_PLAIN, 5.0, (150, 200, 0), 5)
        # cv2.rectangle(frame, *box['left'], (100, 200, 20), thickness=4)
        # cv2.rectangle(frame, *box['center'], (100, 200, 200), thickness=4)
        # cv2.rectangle(frame, *box['right'], (200, 100, 20), thickness=4)

        cv2.imshow('re2', frame)
        k = cv2.waitKey(100) & 0xFF
        if k == 27 or k == ord('q'):
            break


temp_names = {'track': ['tory.jpg', 'tory2.jpg', 'tory3.jpg'],
              'train5': ['pociag5.jpg']}
temp = dict((k, []) for k in temp_names.keys())

for key in temp_names.keys():
    for f in temp_names[key]:
        frame = cv2.imread('wzorce/'+f)
        hist, bins = np.histogram(frame[250:400, 210:300].ravel(), 16, [0, 255])
        temp[key].append(hist)

run_movie(7)
