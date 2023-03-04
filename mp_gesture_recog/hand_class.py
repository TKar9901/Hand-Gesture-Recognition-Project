### MEDIAPIPE HAND MODEL CLASS

### import libraries.
import os
import cv2
import mediapipe as mp
import time
import uuid
import numpy as np

### define class for mediapipe solution.
class HandModel():

	### integrate mediapipe solution via constuctor.
	### --> ie. accesible by all instance-reliant methods.
	def __init__(self, source):
		self.source = "mp_gesture_recog" if source else ""
		self.solutions = mp.solutions
		self.model = self.solutions.hands.Hands(static_image_mode=False, max_num_hands=1)
		self.draw = self.solutions.drawing_utils

	### method for collecting images for training data
	def collectImages(self, IMAGES_PATH, labels, no_imgs):
		for label in labels:
			cap = cv2.VideoCapture(0)
			print(f"images for {label}")
			time.sleep(5)

			for i in range(no_imgs):
				valid = False
				
				while not valid:
					ret, image = cap.read()
					cv2.imshow(f"{label} {i}", image)
					
					if cv2.waitKey(1) == ord("c"):
						valid = self.validateImage(image)

					if cv2.waitKey(1) == ord("q"):
						break

				imgName = os.path.join(self.source, IMAGES_PATH, label+"_"+f"{str(uuid.uuid1())}.jpg")
				cv2.imwrite(imgName, image)

				time.sleep(2.5)

				if cv2.waitKey(1) == ord("q"):
					break

			cap.release()
			cv2.destroyAllWindows()

	### method for validating image landmarks are visible.
	def validateImage(self, image):
		lms = self.model.process(image).multi_hand_landmarks
		if lms:
			return True
		
		return False

	### method for providing normalised average gesture matrix from training data.
	def setGestureMatrices(self, IMAGES_PATH, MATRIX_PATH, labels):
		for label in labels:
			PATH = os.path.join(self.source, IMAGES_PATH)
			for (root, dirs, files) in os.walk(PATH):
				if root == f"{PATH}\\{label}":
					distMatrix = np.zeros((10, 10))
					n=0
					for file in files:
						n += 1

						imgPath = os.path.join(root, file)
						image = cv2.imread(imgPath)

						lm_lst = self.landmarks(image)
						if lm_lst != []:
							imageMatrix = np.array(self.distMatrix(lm_lst, False))

							distMatrix = np.add(distMatrix, imageMatrix)
							distMatrix = self.normaliseMatrix(np.divide(distMatrix, n))

							matPath = os.path.join(self.source, MATRIX_PATH, f"distMatrix_{label}.npy")
							np.save(matPath, distMatrix)

	### method for returning hand landmarks via mediapipe solution.
	def landmarks(self, frame, returnLms=False):
		lms = self.model.process(frame).multi_hand_landmarks
		h, w, c = frame.shape
		lm_lst = []

		if lms:
			for lm in lms:
				for i, l in enumerate(lm.landmark):
					lm_lst.append((int(l.x*w), int(l.y*h)))

		if returnLms:
			return lms, lm_lst
		return lm_lst
		
	### method for annotating image with landmarks. 
	### --> testing purposes
	def annotate(self, frame):
		lms, lm_lst = self.landmarks(frame, True)
		
		if lms:
			for lm in lms:
				self.draw.draw_landmarks(frame, lm, self.solutions.hands.HAND_CONNECTIONS,
					connection_drawing_spec=self.draw.DrawingSpec((0, 255, 0), 2))

			for i in [4, 8, 12, 16, 20]:
				cv2.circle(frame, (lm_lst[i][0], lm_lst[i][1]), 10, (255, 0, 0), cv2.FILLED)

		return frame

	### method for returning distance between any two landmarks.
	def distance(self, lm_lst, a, b):
		import math

		x_diff = lm_lst[a][0] - lm_lst[b][0]
		y_diff = lm_lst[a][1] - lm_lst[b][1]

		dist = math.sqrt(x_diff**2 + y_diff**2)

		return int(dist)

	### method for providing distance matrix from landmarks.
	def distMatrix(self, lm_lst, normalise=True):
		distMatrix = []
		keyPoints = [0, 4, 5, 8, 9, 12, 13, 16, 17, 20]

		for n in keyPoints:
			dists = []
			for m in keyPoints:
				dists.append(self.distance(lm_lst, n, m))

			distMatrix.append(dists)

		if normalise:
			return self.normaliseMatrix(distMatrix)
		else:
			return distMatrix

	### method for normalising given distance matrix such that distances become ratios.
	def normaliseMatrix(self, matrix):
		matrix = np.array(matrix)
		minval, maxval = matrix.min(), matrix.max()

		normalised = np.around((((matrix-minval)/(maxval-minval))*100), 2)
		
		return normalised

	### method for returning sum of errors between any two matrices.
	def calcError(self, distMatrix, gestMatrix):
		errorMatrix = np.abs(np.subtract(np.array(distMatrix), np.array(gestMatrix)))
		error = np.sum(errorMatrix)

		return error

	### method for pulling gesture matrix data from binary file to numpy array.
	def fetchGestureMatrix(self, option, source):
		matPath = os.path.join(self.source, "gestureMatrices", f"distMatrix_{option}.npy")
		distMatrix = np.load(matPath)
		
		return distMatrix

	### method for returning closest match within a custom threshold for any given gesture.
	def deterGesture(self, frame, source):
		lm_lst = self.landmarks(frame)

		options = [
		# label,	error,	threshold,	output
		["palm",	0,		500,		"hello"],
		["fist", 	0, 		2000, 		"goodbye"],
		["rock", 	0, 		600, 		"forex"],
		["peace", 	0, 		600, 		"weather"],
		["like", 	0, 		800, 		"headline"],
		["spock", 	0, 		400, 		"spock"]
		]

		if lm_lst:
			distMatrix = self.distMatrix(lm_lst)

			for option in options:
				gestMatrix = self.fetchGestureMatrix(option[0], source)
				option[1] = self.calcError(distMatrix, gestMatrix)

			bestMatchOrder = sorted(options, key=lambda op:op[1])

			if bestMatchOrder[0][1] < bestMatchOrder[0][2]:
				return bestMatchOrder[0][3]

			return "unknown"
		return "none"

	def gestureOutput(self, gesture):
		end = (gesture == "goodbye") * True

		### imports
		import bbc_feeds
		import requests
		from gtts import gTTS
		from mutagen.mp3 import MP3


		if gesture == "hello":
			output = "welcome to your personal assistant"

		elif gesture == "goodbye":
			output = "thank you for using the personal assistant"

		elif gesture == "forex":
			rate_data = requests.request("GET",
			'https://api.exchangerate.host/convert?from=GBP&to=USD').json()

			output = "exchange rate of 1 GBP to USD is {:.2f}".format(rate_data["info"]["rate"])

		elif gesture == "weather":
			weather_data = requests.request("GET",
			"""https://api.tomorrow.io/v4/weather/forecast?location=london&timesteps=1d&
			units=metric&apikey=eIj2AEBht9V8WkKdoKZ45PIAou8Y1TCr""").json()

			cloud = weather_data["timelines"]["daily"][1]["values"]["cloudCoverAvg"]/100
			precip = weather_data["timelines"]["daily"][1]["values"]["precipitationProbabilityAvg"]
			temp = weather_data["timelines"]["daily"][1]["values"]["temperatureAvg"]

			output = """average london temperature tomorrow is {:.0f} degrees with {:.0%} cloud 
				cover and {:.0%} chance of rain""".format(temp, cloud, precip)

		elif gesture == "headline":
			output = bbc_feeds.news().world()[0]["title"]

		else:
			output = "live long a prosper"
		

		file = f"{self.source}/{gesture}_message.mp3"
		gTTS(output, lang="en").save(file)
		length = MP3(file).info.length

		return file, length, end


