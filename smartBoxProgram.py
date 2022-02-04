#most importantly for this code to run is to import OpenCV which we do in the below line
import cv2
import RPi.GPIO as GPIO
import time
import requests
import json
from model import ResponseApi

#setup para los pines
sensorProxi = 17
channel = 21
channel2 = 20
channel3 = 16
channel4 = 26
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
GPIO.setup(sensorProxi, GPIO.IN) # GPIO Assign mode
GPIO.setup(channel, GPIO.OUT) # GPIO Assign mode
GPIO.setup(channel2, GPIO.OUT) # GPIO Assign mode
GPIO.setup(channel3, GPIO.OUT) # GPIO Assign mode
GPIO.setup(channel4, GPIO.OUT) # GPIO Assign mode
#IMPORTANTE, setear cada locker a HIGH cuando empiece el programa
GPIO.output(channel, GPIO.HIGH)
GPIO.output(channel2, GPIO.HIGH)
GPIO.output(channel3, GPIO.HIGH)
GPIO.output(channel4, GPIO.HIGH)


#Url de api
url = 'http://20.185.1.3:8002/cibi/api/orders-pickup/hash'

# set up camera object called Cap which we will use to find OpenCV
cap = cv2.VideoCapture(0)
# QR code detection Method
detector = cv2.QRCodeDetector()

cerrar_camara = True

future = 0
#This creates an Infinite loop to keep your camera searching for data at all times
def abrirCaja(pin, i):
    print("abrir la caja nro: ", i)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin, GPIO.HIGH)

def checkQR(hash):
    playload = {
        'hash': hash
    }
    data_json = json.dumps(playload)
    try:
        response = requests.post(f'{url}/check', data=data_json)
       
        response_api = ResponseApi(json.loads(response.content.decode()), response.status_code)

        return response_api.content
    except:
        return ResponseApi("Error de conexion", 500)
    
while True:
    time.sleep(0.5)
    now = time.time()
    #print(GPIO.input(sensorProxi))
    if(GPIO.input(sensorProxi) == 1):
        print("activamos camara")
        future = now + 15
        detector = cv2.QRCodeDetector()
        cap = cv2.VideoCapture(0)
        cerrar_camara = False
    
    while cerrar_camara == False:
        #Verificamos si 5 segundos pasaron desde que la camara se prendio
        now = time.time()
        if(now > future):
            print("pasaron 15 segundos")
            cerrar_camara = True
        
        # Below is the method to get a image of the QR code
        _, img = cap.read()
        
        # Below is the method to read the QR code by detetecting the bounding box coords and decoding the hidden QR data 
        data, bbox, _ = detector.detectAndDecode(img)
        
        # This is how we get that Blue Box around our Data. This will draw one, and then Write the Data along with the top (Alter the numbers here to change the colour and thickness of the text)
        if(bbox is not None):
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                         0, 0), thickness=2)
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 250, 120), 2)
            bandera = True
            #Below prints the found data to the below terminal (This we can easily expand on to capture the data to an Excel Sheet)
            #You can also add content to before the pass. Say the system reads red it'll activate a Red LED and the same for Green.
            
            hash = data
            print("hash: ", hash)
            resp = checkQR(hash)
            print("resp: ", resp)
            try: 
                if(resp["box"] == '1'):
                    abrirCaja(channel, 1)
                    cerrar_camara = True
                    data = False
                    
                elif(resp["box"] == '2'):
                    abrirCaja(channel2, 2)
                    cerrar_camara = True
                    data = False
                    
                elif(resp["box"] == '3'):
                    abrirCaja(channel3, 3)
                    cerrar_camara = True
                    data = False
                
                elif(resp["box"] == '4'):
                    abrirCaja(channel4, 4)
                    cerrar_camara = True
                    data = False
                 
                    
            except:
                print("error de lectura QR")
                #time.sleep(0.2)

        # Below will display the live camera feed to the Desktop on Raspberry Pi OS preview
        cv2.imshow("code detector", img)
        
        #At any point if you want to stop the Code all you need to do is press 'q' on your keyboard
        if(cv2.waitKey(1) == ord("q")):
            cerrar_camara = True
            break
        
    if(cerrar_camara == True):
        cap.release()
  
    if(cv2.waitKey(1) == ord("c")):
        detector = cv2.QRCodeDetector()
        cap = cv2.VideoCapture(0)
        cerrar_camara = False     
        
# When the code is stopped the below closes all the applications/windows that the above has created
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()                                                                           
