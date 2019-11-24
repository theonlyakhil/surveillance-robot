

from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import os
from camera import Camera

app = Flask(__name__, template_folder='template')

sensor = Adafruit_DHT.DHT11

DHTpin = 18  # use gpio number not board number for DHT

pirPin = 16

# Wheel controls
m11 = 35  # front left
m12 = 36  # front right
m21 = 37  # back left
m22 = 38  # back right

# UltrasonicSensor
topTrig = 22
topEcho = 21
leftTrig = 24
leftEcho = 23
downTrig = 28
downEcho = 27
rightTrig = 32
rightEcho = 31

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pirPin, GPIO.IN)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.output(m11, 0)
GPIO.output(m12, 0)
GPIO.output(m21, 0)
GPIO.output(m22, 0)


def distance(pinTrig, pinEcho):
    try:
        GPIO.setup(pinTrig, GPIO.OUT)
        GPIO.setup(pinEcho, GPIO.IN)
        GPIO.output(pinTrig, False)
        while GPIO.input(pinEcho) == 0:
            nosig = time.time()

        while GPIO.input(pinEcho) == 1:
            sig = time.time()

        tl = sig - nosig
        distance = tl / 0.000058
        GPIO.cleanup()
        return distance
    except:
        distance = 100
        GPIO.cleanup()
        return distance


a = 1
@app.route("/")
def index():
    GPIO.setmode(GPIO.BOARD)
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHTpin)
    pirValue = GPIO.input(pirPin)
    pir_value = ""

    if pirValue == 1:
        pir_value = "Movement detected"
    else:
        pir_value = "No movement"

    ultFront = distance(topTrig, topEcho)
    ultLeft = distance(leftTrig, leftEcho)
    ultDown = distance(downTrig, downEcho)
    ultRight = distance(rightTrig, rightEcho)

    templateData = {
        'temperature': temperature,
        'humidity': humidity,
        'pir_value': pir_value,
        'ultrasonic_front': ultFront,
        'ultrasonic_left': ultLeft,
        'ultrasonic_down': ultDown,
        'ultrasonic_right': ultRight
    }
    return render_template('robot.html', **templateData)


@app.route('/left_side')
def left_side():
    data1 = "LEFT"
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    return 'true'


@app.route('/right_side')
def right_side():
    data1 = "RIGHT"
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    return 'true'


@app.route('/up_side')
def up_side():
    data1 = "FORWARD"
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    return 'true'


@app.route('/down_side')
def down_side():
    data1 = "BACK"
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    return 'true'


@app.route('/stop')
def stop():
    data1 = "STOP"
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    return 'true'


@app.route('/cam_left')
def cam_left():
    data1 = "Camera Left"
    os.system("python3 servoMotor.py left")
    return 'true'


n = 7.5
@app.route('/cam_right')
def cam_right():
    data1 = "Camera Right"
    os.system("python3 servoMotor.py right")
    return 'true'


@app.route('/cam_stop')
def cam_stop():
    data1 = "Camera stop"
    return 'true'


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    print("start")
    app.run(host='0.0.0.0', port=3000)
