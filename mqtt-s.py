import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import tty
import sys
import termios
import json


class Motor:
    PIN = 18

    PWMA1 = 6
    PWMA2 = 13
    PWMB1 = 20
    PWMB2 = 21
    D1 = 12
    D2 = 26

    PWM = 150

    PWM = 150

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(PWMA1, GPIO.OUT)
    GPIO.setup(PWMA2, GPIO.OUT)
    GPIO.setup(PWMB1, GPIO.OUT)
    GPIO.setup(PWMB2, GPIO.OUT)
    GPIO.setup(D1, GPIO.OUT)
    GPIO.setup(D2, GPIO.OUT)
    p1 = GPIO.PWM(D1, 500)
    p2 = GPIO.PWM(D2, 500)
    p1.start(60)
    p2.start(60)
    def set_motor(self, A1, A2, B1, B2):
        GPIO.output(self.PWMA1, A1)
        GPIO.output(self.PWMA2, A2)
        GPIO.output(self.PWMB1, B1)
        GPIO.output(self.PWMB2, B2)
        print("set motor")


    def forward(self):
        GPIO.output(self.PWMA1, 1)
        GPIO.output(self.PWMA2, 0)
        GPIO.output(self.PWMB1, 1)
        GPIO.output(self.PWMB2, 0)
        print("amamammama")


    def stop(self):
        self.set_motor(0, 0, 0, 0)
        print("stop")

    def reverse(self):
        GPIO.output(self.PWMA1, 0)
        GPIO.output(self.PWMA2, 1)
        GPIO.output(self.PWMB1, 0)
        GPIO.output(self.PWMB2, 1)
        print("reverse")

    def left(self):
        GPIO.output(self.PWMA1, 0)
        GPIO.output(self.PWMA2, 0)
        GPIO.output(self.PWMB1, 0)
        GPIO.output(self.PWMB2, 1)
        print("left")
    def right(self):
        GPIO.output(self.PWMA1, 0)
        GPIO.output(self.PWMA2, 1)
        GPIO.output(self.PWMB1, 0)
        GPIO.output(self.PWMB2, 0)
        print("right")

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("control/motor")


def on_message(client, userdata, msg):
    mt = Motor()
    mt.stop()
    if msg.payload.decode() != "":
        print("Yes!")
        message = str(msg.payload.decode())
        print(message)
        mss = json.loads(message)
        print(mss)
        #forward = int(mss[0])
        #print(str(forward))
        #direction = int(mss[1])
        print("Forward: {} Direction: {}".format(str(mss[0]), str(mss[1])))
        if mss[0] > 10:
            print("power on")
            mt.forward()
        if mss[0] < -10:
            mt.reverse()
        if mss[1] > 10:
            mt.right()
        if mss[1] < - 10:
            mt.left()
        if mss[0] == 0 and mss[1] == 0:
            mt.stop()
#        client.disconnect()


client = mqtt.Client()
client.connect("192.168.1.22", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()