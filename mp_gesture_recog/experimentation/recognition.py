# im not sure what this is.

# import libraries.
import cv2
import os
import mediapipe as mp
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

mp_hands = mp.solutions.hands
hands_model = mp_hands.Hands(max_num_hands=1, static_image_mode=True)
mp_draw = mp.solutions.drawing_utils

mpAPI = [mp_hands, hands_model, mp_draw]

IMAGES_PATH = "collectedImages"

labels = ["palm", "fist", "rock", "peace"]

allData = []

for label in labels:
	for (root, dirs, files) in os.walk(os.path.join(IMAGES_PATH, label)):
		for file in files:
			image = cv2.imread(os.path.join(IMAGES_PATH, label, file))
			
			results = hands_model.process(cv2.rotate(image, cv2.ROTATE_180))
			landmarks = results.multi_hand_landmarks
			
			if landmarks:
				data = []
				for landmark in landmarks:
					for i, lm in enumerate(landmark.landmark):
						data.append((lm.x, lm.y))
				allData.append(data)
			else:
				print(file)
			
			break

# print(allData)


colours = ["r", "g", "b", "y"]
fig = plt.figure()

for i, data in enumerate(allData):
	for (x, y) in data:
		plt.plot(x, y, ".", color=colours[i])


plt.ylim(0, 1)
plt.xlim(0, 1)
plt.show()