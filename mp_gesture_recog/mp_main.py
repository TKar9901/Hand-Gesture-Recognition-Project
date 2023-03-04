### RECOGNITION OF PRESET GESTURES

### import libraries.
import cv2
### import class module from file.
from hand_class import HandModel
mp_model = HandModel(source=0)

### live feed.
cap = cv2.VideoCapture(0)
while True:
	ret, frame = cap.read()
	
	### image manipulation.
	frame = cv2.flip(frame, 1)
	h, w, c = frame.shape

	### recognition from preset gestures.
	gesture = mp_model.deterGesture(frame, source=0)

	# colour format = BGR
	if gesture:
		cv2.putText(img=frame, text=gesture, org=(50, 50), fontScale=1,
			fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(255, 0, 0), thickness=2)

	### feed output and base case.
	cv2.imshow("live feed", frame)
	if cv2.waitKey(1) == ord("q"):
		# print(mp_model.landmarks(frame))
		break

### end live feed.
cap.release()
cv2.destroyAllWindows()



