import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import operator
import requests


def load_videos():
    ''' zwraca liste nazw filmow avi znajdujacych sie katalogu roboczym
        lub w jego subfolderach '''
    video = []
    for root, dir, files in os.walk('.'):
        for file in files:
            if file.endswith('.avi'):
                print(root+file)
                video.append(root+'/'+file)
    return video


def getROItrack(frame):
    ''' przycina obraz do fragmentu gdzie wystepuje pociag '''
    h, w = frame.shape[:2]
    return frame[int(h/1.8):, 15:-120]


def save_frame(cap, number=323, filename='pociag5.jpg'):
    ''' zapisuje dana klatke ze strumienia do pliku '''
    cap.set(cv2.CAP_PROP_POS_FRAMES, number)
    ret, frame = cap.read()
    cv2.imwrite(filename, frame)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


last_train_key = 'track'
def search_train(frame):
    ''' poszukuje pociagu na podanym (oryginalnym) obrazku
        porownujac go do podanych wzorcow ze slownika temp (templates) '''
    global last_train_key
    p1, p2 = (210, 250), (300, 400)
    #cv2.rectangle(frame, p1, p2, (100, 200, 50), thickness=4)
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
    factor = 1.0 / sum(normalised_d.values())
    normalised_d = {k: v*factor for k, v in normalised_d.items()}
    print(normalised_d)
    result = max(normalised_d, key=normalised_d.get)
    last_train_key = result
    return result


def get_video_stream(num):
    ''' pobierz stream nzgodny z numerkiem '''
    if num >= 0:
        video = load_videos()
        cap = cv2.VideoCapture(video[num])
    elif num == -1:
        cap = cv2.VideoCapture(0)
        print(cap)
    elif num == -2:
        url = 'http://192.168.2.1/?action=stream'
        cap = requests.get(url, stream=True)
    else:
        raise Exception("run_movie '>=0' -> video, '-1'->camera, '-2'-camera stream")
    return cap



def get_new_frame(cap):
    ''' pobierz ramkę uwzględniajac rodzaj strumienia '''
    print(type(cap))
    if isinstance(cap, requests.models.Response):
        bytes = cap.raw.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            return True, frame
        else:
            return False, None
    elif cap is not None:
        print('vc')
        ret, frame = cap.read()
        return ret, frame
    else:
        raise Exception('Error')


def run_movie(num):
    cap = get_video_stream(num)
    ret, frame = get_new_frame(cap)
    print(ret, frame)
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
        cv2.putText(frame, str(int(cap.get(cv2.CAP_PROP_POS_FRAMES))), (50, 50), cv2.FONT_HERSHEY_PLAIN, 5.0, (150, 200, 0), 5)
        cv2.putText(frame, train, (50, 100), cv2.FONT_HERSHEY_PLAIN, 5.0, (150, 200, 0), 5)
        # cv2.rectangle(frame, *box['left'], (100, 200, 20), thickness=4)
        # cv2.rectangle(frame, *box['center'], (100, 200, 200), thickness=4)
        # cv2.rectangle(frame, *box['right'], (200, 100, 20), thickness=4)

        cv2.imshow('re2', frame)
        k = cv2.waitKey(100) & 0xFF
        if k == 27 or k == ord('q'):
            break


# zdefiniuj etykiety i miejsce gdzie mozna znaleźć ich wzorce
temp_names = {'track': ['tory.jpg', 'tory2.jpg', 'tory3.jpg', 'tory4.jpg'],
              'train5': ['pociag5.jpg'],
              #'train2': ['pociag2.jpg', 'pociag2-3.jpg']
              }
temp = dict((k, []) for k in temp_names.keys())

# odczytaj wzorce
for key in temp_names.keys():
    for f in temp_names[key]:
        frame = cv2.imread('wzorce/' + f)
        hist, bins = np.histogram(frame[250:400, 210:300].ravel(), 16, [0, 255])
        temp[key].append(hist)

# wystartuj
# -1 -> obraz z domyslnej kamerki systemu
# -2 -> obraz z pociagu
run_movie(-2)



