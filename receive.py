import socket
import RPi.GPIO as GPIO
import time

UDP_IP = "192.168.40.55"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, #Internet
                     socket.SOCK_DGRAM) #UDP
sock.bind((UDP_IP, UDP_PORT))

channel = 21
channel2 = 20
channel3 = 16
channel4 = 26
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
GPIO.setup(channel, GPIO.OUT) # GPIO Assign mode
GPIO.setup(channel2, GPIO.OUT) # GPIO Assign mode
GPIO.setup(channel3, GPIO.OUT) # GPIO Assign mode
GPIO.setup(channel4, GPIO.OUT) # GPIO Assign mode
#IMPORTANTE, setear cada locker a HIGH cuando empiece el programa
GPIO.output(channel, GPIO.HIGH)
GPIO.output(channel2, GPIO.HIGH)
GPIO.output(channel3, GPIO.HIGH)
GPIO.output(channel4, GPIO.HIGH)

def abrirCaja(pin, i):
    print("abrir la caja nro: ", i)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin, GPIO.HIGH)
    
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message:", data.decode())
    try:
        if(data.decode() == "1"):
            abrirCaja(channel, 1)
        elif(data.decode() == "2"):
            abrirCaja(channel2, 2)
        elif(data.decode() == "3"):
            abrirCaja(channel3, 3)
        elif(data.decode() == "4"):
            abrirCaja(channel4, 4)
    except:        
        print("Error en la comunicacion de los RPI")