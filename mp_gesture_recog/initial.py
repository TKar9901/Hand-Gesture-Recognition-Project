### IMAGE COLLECTION FOR TRAINING DATA AND AVERAGE GESTURE MATRICES
### DEFINED FOR REFERENCE

### import libraries.
import os
import numpy as np
import cv2
### import class module from file.
from hand_class import HandModel
mp_model = HandModel()


### image collection.
IMAGES_PATH = "collectedImages"
labels = ["palm", "fist", "rock", "peace", "spock", "like"]
no_imgs = 7

# mp_model.collectImages(IMAGES_PATH, labels, no_imgs)


### gesture matrices defined.
MATRIX_PATH = "gestureMatrices"

# mp_model.setGestureMatrices(IMAGES_PATH, MATRIX_PATH, labels)


