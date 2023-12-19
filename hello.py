from flask import Flask, Response
import cv2 as cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # Captura desde la cámara (cambia el número si tienes varias cámaras)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')


if __name__ == '__main__':
    app.run(debug=True)
