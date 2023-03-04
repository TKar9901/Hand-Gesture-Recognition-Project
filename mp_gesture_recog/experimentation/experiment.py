# experiment in hand-tracking API.

#importing libraries.
import cv2
import mediapipe as mp
import math

# initiating mediapipe hand tracking solution and draw tool.
mp_hands = mp.solutions.hands
hands_model = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils


# defining video capture object.
cap = cv2.VideoCapture(0)

# setting up result images.
like_img = cv2.resize(cv2.imread("images/LIKE.jpg"), (108, 97))
dislike_img = cv2.resize(cv2.imread("images/DISLIKE.jpg"), (108, 97))
peace_img = cv2.resize(cv2.imread("images/PEACE.png"), (105, 105))
rock_img = cv2.resize(cv2.imread("images/ROCK.png"), (105, 105))
middle_img = cv2.resize(cv2.imread("images/MIDDLE.jpg"), (120, 120))
spock_img = cv2.resize(cv2.imread("images/SPOCK.png"), (105, 105))

# PATH = "test_data"
# # main running program.
# # while True:
# for root, dirs, files in os.walk(PATH):
# 	for file in files:
# 		if file == "Picture10.jpg":
# 			frame = cv2.imread(os.path.join(root, file))
# 			# collecting real-time data.
# 			# ret, frame = cap.read()
# 			# frame = cv2.flip(frame, 1)
# 			h, w, c = frame.shape
# 			results = hands_model.process(frame)
# 			landmarks = results.multi_hand_landmarks
			

# 			# using drawing tool to display landmarks.
# 			if landmarks:
# 				for landmark in landmarks:
# 					mp_draw.draw_landmarks(frame, landmark, mp_hands.HAND_CONNECTIONS,
# 						connection_drawing_spec=mp_draw.DrawingSpec((0, 255, 0), 2))

# 			cv2.imwrite(os.path.join(PATH, "z_"+file), frame)


# main running program.
while True:

	# collecting real-time data.
	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)
	h, w, c = frame.shape
	results = hands_model.process(frame)
	landmarks = results.multi_hand_landmarks
	

	# using drawing tool to display landmarks.
	if landmarks:
		for landmark in landmarks:
			mp_draw.draw_landmarks(frame, landmark, mp_hands.HAND_CONNECTIONS,
				connection_drawing_spec=mp_draw.DrawingSpec((0, 255, 0), 2))

			
			lm_lst =[]
			for i, lm in enumerate(landmark.landmark):
				lm_lst.append((int(lm.x*w), int(lm.y*h)))


			# check if each finger is folded.
			true = []
			for i in [8, 12, 16, 20]:
				
				distTto0 = math.sqrt((lm_lst[i][0]-lm_lst[0][0])**2 + (lm_lst[i][1]-lm_lst[0][1])**2)

				distKto0 = math.sqrt((lm_lst[i-3][0]-lm_lst[0][0])**2 + (lm_lst[i-3][1]-lm_lst[0][1])**2)

				if distTto0 > distKto0:
					cv2.circle(frame, (lm_lst[i][0], lm_lst[i][1]), 10, (255, 0, 0), cv2.FILLED)
				else:
					cv2.circle(frame, (lm_lst[i][0], lm_lst[i][1]), 10, (0, 0, 255), cv2.FILLED)
					true.append(i)

			
			# check if it is thumbs up or down.
			if true == [8, 12, 16, 20]:

				if (lm_lst[4][1] < lm_lst[3][1]) and ((lm_lst[4][0] - lm_lst[3][0])**2 < 350):
					# print("thumbs up")
					h, w, c = like_img.shape
					frame[20:h+20, 20:w+20] = like_img
				elif (lm_lst[4][1] > lm_lst[3][1]) and ((lm_lst[4][0] - lm_lst[3][0])**2 < 350):
					# print("thumbs down")
					h, w, c = dislike_img.shape
					frame[20:h+20, 20:w+20] = dislike_img
			

			# check if it is peace sign.
			elif true == [16, 20]:

				dist4To17 = math.sqrt((lm_lst[4][0]-lm_lst[17][0])**2 + (lm_lst[4][1]-lm_lst[17][1])**2)
				dist5To17 = math.sqrt((lm_lst[5][0]-lm_lst[17][0])**2 + (lm_lst[5][1]-lm_lst[17][1])**2)

				if dist4To17 < dist5To17:
					straight = True
					for tip in [8, 12]:
						if not(lm_lst[tip][1] < lm_lst[tip-1][1] < lm_lst[tip-2][1] < lm_lst[tip-3][1]):
							straight = False
					if straight:
						# print("peace sign")
						h, w, c = peace_img.shape
						frame[20:h+20, 20:w+20] = peace_img
			

			# check if it is rock sign.
			elif true == [12, 16]:

				straight = True
				for tip in [8, 20]:
					if not(lm_lst[tip][1] < lm_lst[tip-1][1] < lm_lst[tip-2][1] < lm_lst[tip-3][1]):
						straight = False
				if straight:
					# print("rock sign")
					h, w, c = rock_img.shape
					frame[20:h+20, 20:w+20] = rock_img
			

			# check if it is middle finger.
			elif true == [8, 16, 20]:

				dist4To17 = math.sqrt((lm_lst[4][0]-lm_lst[17][0])**2 + (lm_lst[4][1]-lm_lst[17][1])**2)
				dist5To17 = math.sqrt((lm_lst[5][0]-lm_lst[17][0])**2 + (lm_lst[5][1]-lm_lst[17][1])**2)

				if dist4To17 < dist5To17:
					if lm_lst[12][1] < lm_lst[11][1] < lm_lst[10][1] < lm_lst[9][1]:
						# print("middle finger")
						h, w, c = middle_img.shape
						frame[20:h+20, 20:w+20] = middle_img
			

			# check if it is spock sign.
			else:
				# average distance between outer bases < distance between inner bases
				# + average distance between outer tips < distance between inner tips
				
				dist5To9 = math.sqrt((lm_lst[5][0]-lm_lst[9][0])**2 + (lm_lst[5][1]-lm_lst[9][1])**2)
				dist13To17 = math.sqrt((lm_lst[13][0]-lm_lst[17][0])**2 + (lm_lst[13][1]-lm_lst[17][1])**2)
				av_base_dist = (dist5To9 + dist13To17)/2
				
				dist8To12 = math.sqrt((lm_lst[8][0]-lm_lst[12][0])**2 + (lm_lst[8][1]-lm_lst[12][1])**2)
				dist16To20 = math.sqrt((lm_lst[16][0]-lm_lst[20][0])**2 + (lm_lst[16][1]-lm_lst[20][1])**2)
				av_tip_dist = (dist8To12 + dist16To20)/2

				dist9To13 = math.sqrt((lm_lst[9][0]-lm_lst[13][0])**2 + (lm_lst[9][1]-lm_lst[13][1])**2)
				dist12To16 = math.sqrt((lm_lst[12][0]-lm_lst[16][0])**2 + (lm_lst[12][1]-lm_lst[16][1])**2)

				if (dist9To13 > av_base_dist/2) and (dist12To16 > 1.5*av_tip_dist):
					straight = True
					for tip in [8, 12, 16, 20]:
						if not(lm_lst[tip][1] < lm_lst[tip-1][1] < lm_lst[tip-2][1] < lm_lst[tip-3][1]):
							straight = False
					if straight:
						# print("spock sign")
						h, w, c = spock_img.shape
						frame[20:h+20, 20:w+20] = spock_img



	# output feed and recall.
	cv2.imshow("live feed", frame)
	if cv2.waitKey(1) == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()
