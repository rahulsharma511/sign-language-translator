import cv2
import os
from os.path import isfile, join
import tensorflow as tf
from utils import detector_utils as detector_utils
import numpy as np


print('>> loading frozen model..')
detection_graph, sess = detector_utils.load_inference_graph()
sess = tf.Session(graph=detection_graph)
print('>> model loaded!')

print(os.listdir("significant-asl-sign-language-alphabet-dataset/Training Set/"))

poses = os.listdir('significant-asl-sign-language-alphabet-dataset/Training Set/')
_iter=1
for pose in poses:
        files = os.listdir('significant-asl-sign-language-alphabet-dataset/Training Set/' + pose + '/')
        print(">> Working on examples : " + pose)
        _iter=1
        for file in files:
            if(file.endswith(".png")):
                path = 'significant-asl-sign-language-alphabet-dataset/Training Set/' + pose + '/' + file
                # Read image
                frame = cv2.imread(path)
                frame = cv2.resize(frame, (320, 180), interpolation=cv2.INTER_AREA)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Detect object
                boxes, scores = detector_utils.detect_objects(frame, detection_graph, sess)
                # get region of interest
                res = detector_utils.get_box_image(1, 0.2, scores, boxes, 320, 180, frame)
                # Save cropped image 
                if(res is not None):
                    cv2.imwrite(path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    print('   Processing '+ pose + str(_iter) + ' frame!')
                    _iter+=1

