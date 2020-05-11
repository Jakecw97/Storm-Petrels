#To fine tune the motion detection, user should change the gaussianBlur, cv2.threshold, cv2.dilate and contourArea variables until they find a sensitivity they see fit

import cv2 #Used for image processing
import imutils
import time
import numpy as np
from imutils.video import VideoStream #Used for reading the stream
from datetime import datetime, timedelta #Used for time

class VideoCamera(object):
    def __init__(self, instance=0):  #initiliases the camera based on instance passed through
        self.vs = VideoStream(src=instance).start() #Begins video stream
        self.instance = instance #Stores instance
        self.timer = 0 #Instance timer
        self.captureTimeout = 3 #Instance capture timeout timer
        time.sleep(2.0) #timeOut to warm up stream
        self.initialFrame=None #Null first frame
        self.movementDetected = False #If movement is detected
        self.lastMovementTime = datetime.now() #Stores the time last movement was detected
        #self.video_writer = cv2.VideoWriter()
        #self.isRecording = False

    def __del__(self):
        self.vs.stop() #Stops stream

    def get_movement(self):
        while True:	#While being called
            frame = self.vs.read() #Sets frame = the newest frame read from stream
            frameCopy=self.vs.read() #Copies the frame, this is used to provide a clean frame
            currentTime = datetime.now()#Set current time
            camName = str(self.instance+1) #Sets a true camera number variable, casts to string to return for displaying on frame in a later line
            frame = imutils.resize(frame, width=500) #Resizes the frame for proeccessing
            frameCopy = imutils.resize(frame, width=500) #Resizes the copy frame to match
   
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts the frame to grayscale
            grayFrame = cv2.GaussianBlur(grayFrame,(21,21),0) #Blurs the frame, helps to remover noise etc.
    
            if  self.initialFrame is None :   #If initialFrame is empty then set it to grayFrame
                self.initialFrame = grayFrame
                continue
    
            if currentTime > self.lastMovementTime + timedelta(seconds=1):   #Timer for X seconds after last movement.
            	self.initialFrame = grayFrame #Set initial frame to grayFrame, this updates the initial frame every 1 second, preventing the program from comparing against a single static frame, and thus tracking movement, rather than a single change
            	self.lastMovementTime = datetime.now() #Set the lastMovement timer to now
            	self.movementDetected = True #Set Movement to true
            
            deltaFrame = cv2.absdiff(self.initialFrame,grayFrame) #Compare the abstract difference between the two frames
            deltaThreshold = cv2.threshold(deltaFrame,30,255,cv2.THRESH_BINARY)[1] #threshold the delta frame
            deltaThreshold = cv2.dilate(deltaThreshold, None, iterations=3) #Refines the image
    
            (contours,_) = cv2.findContours(deltaThreshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Finds contours and adds them to array
    
            for contour in contours: #Loops throught the contours
                if cv2.contourArea(contour) < 1000: #If the contour is smaller than 1000 then disregard it
                    continue
                (x, y, w, h) = cv2.boundingRect(contour) #Add a rectangle around the contour
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 3) #Draw the rectangle onto the frame,  edit the rgb to change it's colour, the final int controls its thickness 
                
                if self.movementDetected is True and (time.time() - self.timer) > self.captureTimeout:  #If movement is detected and if more seconds than the timeout have passed
                     self.timer = time.time() #reset the timer
                     timeString = datetime.now().strftime("%Y_%m_%d-%H %M %S") #Print the current time
                     cv2.imwrite('static/gallery/'+timeString+'_Cam'+camName+'.jpg',frameCopy) #Output image with current time and camera name 
                     self.movementDetected = False #Set movementDetected to false

# Unimplemented, buggy video recording code. Initially planned to record for X seconds upon movement detection, however the videoWriter(s) output empty/invalid 5.7kb sized files. Possible codec error.                     
#                if self.movementDetected is True and self.isRecording is False:
#                     camName = str(self.instance+1)
#                     timeString = datetime.now().strftime("%Y_%m_%d-%H %M %S")
#                     codec = cv2.VideoWriter_fourcc(*'XVID')
#                     self.video_writer= cv2.VideoWriter('gallery/'+timeString+'_Cam'+camName+'.avi',codec, 24.0, (375,500))
                     
#                    self.video_writer.write(frameCopy)
#                     if cv2.waitKey(1) & 0xFF == ord('q'):
#                        break
#                               self.isRecording = True
            #For the live stream
            cv2.putText(frame, "Camera: "+camName, (10, frame.shape[0] - 10), #Add text to the canvas
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1) #Initialise the font, size and colour
                         
            ret, jpeg = cv2.imencode('.jpg', frame) #Return frame as jpg
            return jpeg.tobytes() #Return jpeg to bytes
      
