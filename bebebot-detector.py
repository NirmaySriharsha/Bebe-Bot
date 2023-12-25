#### Bebe-Bot Cat Detector (using Tensorflow on a Raspbery Pi equipped with a PiCamera) ####
### Author: Nirmay Sriharsha Singaram
### Date: 10/6/2023
### Code adapted from Evan Juras' github. 
### https://github.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi/blob/master/README.md
### This script runs with the PiCamera and uses Tensorflow's objection detection to detect objects (of your choice) and save images of them. 
### A javascript script running in tandem then sends this image off as a whatsapp message.

#Imports
import os
import argparse
import cv2
import sys
import time
from picamera2 import Picamera2
import numpy as np
import tensorflow as tf
from PIL import Image
#Import utilities
from utils import label_map_util
from utils import visualization_utils as vis_util

#Camera resolution
IM_WIDTH = 1280
IM_HEIGHT = 720

#Passing in arguments for visualization, confidence level and cooldown time
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--visualize', nargs = "?", const = True, default = False, type = bool, help = "Add -v tag to visualize camera feed and object detection")
parser.add_argument('-c', '--confidence', nargs = "?", default = 0.55, type = float, help = "-c tag takes in floats b/w 0 and 1 to indicate minimum detection confidence required to send message")
parser.add_argument('-f', '--frequency', nargs = "?", default = 5, help = "how frequent (in hours) you would like messages to be sent")
parser.add_argument('-w', '--wait', nargs = "?", default = 5, type = int, help = "how many frames to wait after object detection to take capture")
parser.add_argument('-t', '--testing', nargs = "?", default = False, type = bool, const = True, help = "Run program to detect people (instead of cats) with relaxed frequency and confidence levels for testing purposes")
args = parser.parse_args()
testing = args.testing
visualize, confidence, cooldown, wait = args.visualize, args.confidence, args.frequency*60.0*60.0, args.wait #frequency converted to seconds
print("Visualization is set to ", visualize)
if testing: cooldown = 20
#Move up directory level
sys.path.append("..")
#Location of the model
MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
#Current Working Directory
CWD_PATH = os.getcwd()

#Move to the model! The graph .pb file contains the model that runs the actual object detection. 
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
#Path to the labels outputted by the model
PATH_TO_LABELS = os.path.join(CWD_PATH,'data','mscoco_label_map.pbtxt') 
# Number of classes the object detector can identify
NUM_CLASSES = 90

## Load the label map.
# Label maps map indices to category names, so that when the convolution
# network predicts `5`, we know that this corresponds to `airplane`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
# Label for what we want - cat is 17.0 and dog is 18.0
# Refer to https://gist.github.com/aallan/fbdf008cffd1e08a619ad11a02b74fa8 for the full label dictionary
target_label = 17.0

#Load the Tensorflow model
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.compat.v2.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    sess = tf.compat.v1.Session(graph = detection_graph)



# Define input and output tensors (i.e. data) for the object detection classifier
# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

#Frame Rate Calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX
last_detect = -cooldown - 1 #so that you don't have to wait 7 hours for the first message. 
frames_detected = 0 #Counts number of frames the object is being detected for

#Initialize the camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration({"size":(1024, 768)}))
camera.start()
camera.framerate = 10
#The continuous capture loop
while True:
    frame = camera.capture_array("main")
    t1 = cv2.getTickCount()
    #Process the frame to fit cv's requirements
    frame_cv = np.array(frame)
    frame_cv.setflags(write = 1)
    #Color channel differences between various packages
    frame_cv = cv2.cvtColor(frame_cv, cv2.COLOR_BGR2RGB)
    #Expand frame to run model on it
    frame_expanded = np.expand_dims(frame_cv, axis = 0)
    
    #Actual detection happens here
    (boxes, scores, classes, num) = sess.run(  
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})
    
    #Check for detected objects
    #Class label of 17 is 'cat', 1 is 'person'. For testing purposes, we could look out for people as well, if you don't want to bother your cat.
    #We check if a cat (or a person) is detected with a certain confidence. 
    if (classes[0][0] == 1.0 and scores[0][0] > 0.8 and testing) or (target_label in classes[0] and scores[0][list(classes[0]).index(target_label)] > confidence):
        #Update number of frames the object has been in frame.
        #In order to prevent blurry pics, we wait for the object to be detected for 10 frames (approx 3 seconds) for a clear pic before acting
        frames_detected = frames_detected+1
        #We now check if the gap between messages sent has been long enough (to not be spammy and annoying)
        if frames_detected >= wait:
            im = Image.fromarray(frame)
            if time.time() - last_detect > cooldown:
                last_detect = time.time()
                #Save the image!
                im = Image.fromarray(frame)
                im.save("Results/output.png")
                #At this point our javascript program will automatically send the image to whatsapp
                frames_detected = 0
    else:
        frames_detected = 0
    #Visualize the results (if -v tag is set)
    if visualize:
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame_cv,
            np.squeeze(boxes), 
            np.squeeze(classes).astype(np.int32), 
            np.squeeze(scores), 
            category_index, 
            use_normalized_coordinates = True,
            line_thickness = 8, 
            min_score_thresh = 0.40
        )
        cv2.putText(frame_cv,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
        cv2.imshow("Object Detector", frame_cv)
    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc = 1/time1
    #Press q to quit
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
    

