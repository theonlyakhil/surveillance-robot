

from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time
import Adafruit_DHT

app = Flask(__name__, template_folder='template')
sensor = Adafruit_DHT.DHT11
DHTpin = 18  # use gpio number not board number for DHT
pirPin = 16
servoPin = 8

# Wheel controls
m11 = 35  # front left
m12 = 36  # front right
m21 = 37  # back left
m22 = 38  # back right

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pirPin, GPIO.IN)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.setup(servoPin, GPIO.OUT)
GPIO.output(m11, 0)
GPIO.output(m12, 0)
GPIO.output(m21, 0)
GPIO.output(m22, 0)
p = GPIO.PWM(servoPin, 50)

print("done")

a = 1
@app.route("/")
def index():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHTpin)
    p.start(2.5)
    pirValue = GPIO.input(pirPin)
    pir_value = ""
    if pirValue == 1:
        pir_value = "Movement detected"
    else:
        pir_value = "No movement"
    templateData = {
        'temperature': temperature,
        'humidity': humidity,
        'pir_value': pir_value
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


# @app.route('/cam_left')
# def cam_left():
#     data1 = "Camera Left"
#     return 'true'


# @app.route('/cam_right')
# def cam_right():
#     data1 = "Camera Right"
#     return 'true'


if __name__ == "__main__":
    print("start")
    app.run(host='0.0.0.0', port=3000)
