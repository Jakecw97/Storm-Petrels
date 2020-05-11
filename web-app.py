import cv2 #video processing
import sys
import time
import threading
import os
from mail import sendEmail #To send email updates
from flask import Flask, render_template, Response, request #Flask webserver
from camera import VideoCamera #Import camera
from flask_basicauth import BasicAuth #Basic web authentication
from gevent.pywsgi import WSGIServer #Wsgi server


#Cameras are initialised as NTSC, must be changed to PAL standard
os.system("v4l2-ctl -d /dev/video0 --set-standard 5")
os.system("v4l2-ctl -d /dev/video1 --set-standard 5")
video_camera = VideoCamera(instance = 0) #Initialises camera 1
video_camera2 = VideoCamera(instance = 1) #Initilises camera 2
#To add cameras, create more of the above statements, replace the X with the number of the next camera: 'dev/videoX' and 'instance = X' => dev/video2' and 'instance = 2' and so on

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin' #Reccommend to customise before deployment
app.config['BASIC_AUTH_PASSWORD'] = 'changebeforedeployment'


basic_auth = BasicAuth(app) #initialises basicAuth
emailTimer = 1800 #Every 1800 seconds / 30 Minutes
timer = 0



@app.route('/')
@basic_auth.required #Requires authentication on this page
def index():
    return render_template('index.html') #Renders index.html

def stream(camera):
    while True:   #While being called 
        frame = camera.get_movement() #Call get_movement in camera instance
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') #Return a frame with captured frame

@app.route('/video_feed')    
@basic_auth.required #Requires authentication on this page
def video_feed():  #If scaling to include more cameras, recreate this function with respective camera instance
    return Response(stream(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame') #replace frame, in this case we display on html as image
@app.route('/video_feed2')
@basic_auth.required #Requires authentication on this page
def video_feed2():
    return Response(stream(video_camera2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gallery')
@basic_auth.required #Requires authentication on this page
def gallery():
    images = os.listdir('static/gallery') #Lists everything in the static/gallery folder
    return render_template('gallery.html', images = images) #Renders the page, passes through the list

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False) #Development server
    #deployServer = WSGIServer(('0.0.0.0', 5000), app) #Deployment server (0.0.0.0) allows outward access. To allow remote access, port 5000 should be opened on your router !!Do so at your own risk!!
    #deployServer.serve_forever() #Deploy / Serve forever, no timeouts
