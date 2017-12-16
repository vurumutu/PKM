#!/usr/bin/env python
from flask import Flask, render_template, Response
from camera import Camera, ImageAnalyzer

# wybierz kamere:
#   -2 -> pociag
#   -1 -> kamera systemowa
#   0+ -> numer .avi z aktualnego folderu
cam = Camera(-1)
ia = ImageAnalyzer()
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        res, frame = cam.get_new_frame()
        label = ia.analyze(frame)
        ia.draw_result(frame, label, cam.frame_counter)
        bytes = cam.to_bytes(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    print('response')
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)


