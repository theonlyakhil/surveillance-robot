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
    p.start(n)
    direction = sys.argv[1]
    if direction == "left":
        if n < 15:
            n += 2
            p.ChangeDutyCycle(n)
        else:
            exit
    elif direction == "right":
        if n > 1:
            n -= 2
            p.ChangeDutyCycle(n)
        else:
            exit
    file = open("servoStatus.txt", "w")
    file.write(str(n))
    file.close()


if __name__ == "__main__":
    main()
