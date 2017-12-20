import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import operator
import requests


class Camera:
    ''' kamera z kamery domyslnej, streama lub pliku
        rowniez konwersja do niarmego jpega '''

    def __init__(self, num):
        self.stream_bytes = b''
        self.cap = self.get_video_stream(num)
        self.frame_counter = -1

    @staticmethod
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

    def get_video_stream(self, num):
        ''' pobierz stream nzgodny z numerkiem '''
        if num >= 0:
            video = self.load_videos()
            cap = cv2.VideoCapture(video[num])
        elif num == -1:
            cap = cv2.VideoCapture(0)
            print(cap)
        elif num == -2:
            url = 'http://192.168.2.1/?action=stream'
            print('camera request ', url)
            cap = requests.get(url, stream=True)
            print('camera request ready')
        elif num == -3:
            url = 'http://127.0.0.1:5000/video_feed'
            print('camera request ', url)
            cap = requests.get(url, stream=True)
            print('camera request ready')
        else:
            raise Exception("run_movie '>=0' -> video, '-1'->camera, '-2'-camera stream")
        return cap

    def get_new_frame(self):
        ''' pobierz ramkę uwzględniajac rodzaj strumienia '''
        if isinstance(self.cap, requests.models.Response):
            self.stream_bytes += self.cap.raw.read(1024)
            a = self.stream_bytes.find('\xff\xd8')
            b = self.stream_bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                jpg = self.stream_bytes[a:b + 2]
                self.stream_bytes = self.stream_bytes[b + 2:]
                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                return True, frame
            else:
                return False, None
        elif self.cap is not None:
            self.frame_counter = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            ret, frame = self.cap.read()
            if self.frame_counter >= self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return ret, frame
        else:
            raise Exception('Error')

    @staticmethod
    def to_bytes(frame):
        ''' konwertuje obraz do binarnego jpega '''
        ret, frame = cv2.imencode('.jpg', frame)
        return frame.tobytes()

    def save_frame(self, number=323, filename='pociag5.jpg'):
        ''' zapisuje dana klatke ze strumienia do pliku '''
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, number)
        ret, frame = self.cap.read()
        cv2.imwrite(filename, frame)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


class ImageAnalyzer:
    ''' poszukiwanie pociagow '''

    def __init__(self):
        # zdefiniuj etykiety i miejsce gdzie mozna znaleźć ich wzorce
        temp_names = {'track': ['tory.jpg', 'tory2.jpg', 'tory3.jpg', 'tory4.jpg'],
                      'train5': ['pociag5.jpg'],
                      #'train2': ['pociag2.jpg', 'pociag2-3.jpg']
                      }
        self.templates = dict((k, []) for k in temp_names.keys())
        self.last_train_key = list(self.templates.keys())[0]
        print(self.last_train_key)

        # odczytaj wzorce
        for key in temp_names.keys():
            for f in temp_names[key]:
                frame = cv2.imread('wzorce/' + f)
                hist, bins = np.histogram(frame[250:400, 210:300].ravel(), 16, [0, 255])
                self.templates[key].append(hist)

    def getROItrack(self, frame):
        ''' przycina obraz do fragmentu gdzie wystepuje pociag '''
        h, w = frame.shape[:2]
        return frame[int(h / 1.8):, 15:-120]

    def search_train(self, frame):
        ''' poszukuje pociagu na podanym (oryginalnym) obrazku
            porownujac go do podanych wzorcow ze slownika temp (templates)
             zwraca etykiete rezultatu '''
        p1, p2 = (210, 250), (300, 400)
        #cv2.rectangle(frame, p1, p2, (100, 200, 50), thickness=4)
        roi = frame[250:400, 210:300]
        hist, bins = np.histogram(roi.ravel(), 16, [0, 255])
        values = dict((k, float('inf')) for k in self.templates.keys())
        for key in self.templates.keys():
            for i in range(len(self.templates[key])):
                dist = np.linalg.norm(hist - self.templates[key][i])
                values[key] = min(values[key], dist)
        values[self.last_train_key] *= 0.9  # histereza
        factor = 1.0 / sum(values.values())
        normalised_d = {k: (1-v * factor) for k, v in values.items()}
        factor = 1.0 / sum(normalised_d.values())
        normalised_d = {k: v*factor for k, v in normalised_d.items()}
        print(normalised_d)
        result = max(normalised_d, key=normalised_d.get)
        self.last_train_key = result
        return result

    @staticmethod
    def draw_result(frame, result, frame_nbr=None):
        ''' dodaje napis do ramki obrazka '''
        if frame_nbr is not None:
            cv2.putText(frame, str(int(frame_nbr)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 5.0, (150, 200, 0), 5)
        cv2.putText(frame, str(result['label']), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5.0, (150, 200, 0), 5)

    def analyze(self, frame):
        label = self.search_train(frame)
        result = {'label': label}
        return result


def run_movie(num):
    cam = Camera(num)
    ia = ImageAnalyzer()
    ret, frame = cam.get_new_frame()
    frame = ia.getROItrack(frame)
    h, w = frame.shape[:2]
    box_size = int(w/5)
    os = int(w/2) - int(box_size/1.5)
    box = {'left': ((os-box_size, h), (os, h-box_size)),
           'center': ((int(os-box_size/2), h), (int(os+box_size/2), h-box_size)),
            'right': ((os, h), (os+box_size, h-box_size))}
    while True:
        ret, frame = cam.get_new_frame()
        if ret != True:
            break

        result = ia.analyze(frame)
        ia.draw_result(frame, result, cam.frame_counter)
        # cv2.rectangle(frame, *box['left'], (100, 200, 20), thickness=4)
        # cv2.rectangle(frame, *box['center'], (100, 200, 200), thickness=4)
        # cv2.rectangle(frame, *box['right'], (200, 100, 20), thickness=4)

        cv2.imshow('re2', frame)
        k = cv2.waitKey(100) & 0xFF
        if k == 27 or k == ord('q'):
            break

if __name__=='__main__':
    run_movie(-1)



