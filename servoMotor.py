import sys
import RPi.GPIO as GPIO

servoPin = 8
p = GPIO.PWM(servoPin, 50)


def main():
    file = open("servoStatus.txt", "r")
    n = int(file)
    file.close()
    direction = sys.argv[1]
    if direction == "left":
        n += 0.5
        p.ChangeDutyCycle(n)
    elif direction == "right":
        n -= 0.5
        p.ChangeDutyCycle(n)
    file = open("servoStatus.txt", "w")
    file.write(n)


if __name__ == "__main__":
    main()
