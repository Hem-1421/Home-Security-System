import cv2
import sys
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading
import datetime 
import pytz 
import telepot
from urllib.request import urlopen
import sys

WRITE_API = "WXH40ZF14XYYB0VH" # Replace your ThingSpeak API key here
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)
 
thingspeakHttp = BASE_URL + "&field3=Starting_all_clear"
print(thingspeakHttp)

conn = urlopen(thingspeakHttp)
print("Response: {}".format(conn.read()))
conn.close()

import pyrebase
config = {
    "apiKey": "AIzaSyDXIFK_2BJzvX65BO2as3yQ6XEmXaEy1Do",
  "authDomain": "iot-proj-camera.firebaseapp.com",
  "databaseURL": "https://iot-proj-camera-default-rtdb.firebaseio.com",  
  "storageBucket": "iot-proj-camera.appspot.com" 
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

token = '2102327904:AAFsSJ8zLe8VOzdAH36nio0qh2VypyEKwbM' # telegram token
receiver_id = 989221812 # https://api.telegram.org/bot<TOKEN>/getUpdates
bot = telepot.Bot(token)
current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
bot.sendMessage(receiver_id, 'Stating @ '+str(current_time)) # send a activation message to telegram receiver id


def send_message(strg):
    bot.sendMessage(receiver_id, strg)
    thingspeakHttp = BASE_URL + "&field3=Breach_detected"
    print(thingspeakHttp)

    conn = urlopen(thingspeakHttp)
    print("Response: {}".format(conn.read()))
    conn.close()
    data_1 = {
    "Message": strg,
  
    }
    db.push(data_1)



email_update_interval = 1 # sends an email only once in this time interval
video_camera = VideoCamera(flip=True) # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml") # an opencv classifier

# App Globals (do not edit)
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'pi'
app.config['BASIC_AUTH_PASSWORD'] = '0000'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0


def check_for_objects():
	global last_epoch
	while True:
		try:
			frame, found_obj = video_camera.get_object(object_classifier)
			if found_obj and (time.time() - last_epoch) > email_update_interval:
				last_epoch = time.time()
				print ("Sending Alert")
				bot.sendPhoto(receiver_id, photo=open('Frame.jpg', 'rb'))
				send_message("breach detected @ "+str(current_time))
				print ("breach detected @ "+str(current_time)+" -- Alert sent")
				#camera.capture('picture.jpg')
		except:
			print ("Error sending email: ", sys.exc_info()[0])

@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
