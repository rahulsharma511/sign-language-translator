import cv2, pickle
import numpy as np
import tensorflow as tf
#from cnn_tf import cnn_model_fn
import os
import sqlite3, pyttsx3
from keras.models import load_model
from threading import Thread

engine = pyttsx3.init()
engine.setProperty('rate', 150)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#model = load_model('cnn_model_keras2.h5')
prediction = list("SOCXTVRLHEIAGPZJDQMWKYBNFU")

#x, y, w, h = 300, 100, 300, 300
is_voice_on = True


def say_text(text):
	if not is_voice_on:
		return
	while engine._inLoop:
		pass
	engine.say(text)
	engine.runAndWait()

def text_mode(cam, count_same_frame,text,word):
	global is_voice_on
	if cam is not None:
		old_text = text[0]
		text[0] = prediction[cam.argmax()]
		if old_text == text[0]:
			count_same_frame[0] += 1
		else:
			count_same_frame[0] = 0
		if count_same_frame[0] > 10:
			if len(text[0]) == 1:
				Thread(target=say_text, args=(text[0], )).start()
			word[0] = word[0] + text[0]
			if word[0].startswith('I/Me '):
				word[0] = word[0].replace('I/Me ', 'I ')
			elif word[0].endswith('I/Me '):
				word[0] = word[0].replace('I/Me ', 'me ')
			count_same_frame[0] = 0
		blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
		cv2.putText(blackboard, "Text Mode", (180, 50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255, 0,0))
		cv2.putText(blackboard, "Predicted text- " + text[0], (30, 100), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 0))
		cv2.putText(blackboard, word[0], (30, 240), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255))
		if is_voice_on:
			cv2.putText(blackboard, "Voice on", (450, 440), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 127, 0))
		else:
			cv2.putText(blackboard, "Voice off", (450, 440), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 127, 0))
		
		cv2.imshow("Recognizing gesture", blackboard)
		keypress = cv2.waitKey(1)
		if keypress == ord('v') and is_voice_on:
			is_voice_on = False
		elif keypress == ord('v') and not is_voice_on:
			is_voice_on = True
		elif keypress == ord('c'):
			word[0] = ''
		elif keypress == ord(' '):
			word[0] += ' '






















