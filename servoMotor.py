import sys
import RPi.GPIO as GPIO

servoPin = 8
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin, GPIO.OUT)
p = GPIO.PWM(servoPin, 50)


def main():
    file = open("servoStatus.txt", "r")
    y = file.read()
    n = int(y)
    file.close()
    print(n)
    p.start(n)
    direction = sys.argv[1]
    if direction == "left":
        n += 2
        p.ChangeDutyCycle(n)
        print(n)
    elif direction == "right":
        n -= 2
        p.ChangeDutyCycle(n)
    file = open("servoStatus.txt", "w")
    file.write(str(n))
    file.close()


if __name__ == "__main__":
    main()
