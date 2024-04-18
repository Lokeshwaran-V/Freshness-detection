from __future__ import division
import io
import os
import random
import cv2
import numpy as np
import time
from copy import deepcopy
from PIL import Image

kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

# The name of the image file to annotate
i = time.strftime("%d-%m-%y_%H-%M-%S")

image = np.array(Image.open('test_apple.jpg'))
# image = np.array(Image.open('test_green_apple.jpg'))
# image = np.array(Image.open('test_black_apple.jpeg'))
# image = np.array(Image.open('test_black.jpeg'))
# image = np.array(Image.open('test_banana.jpeg'))

frame = image
edge_img = deepcopy(image)
# finds edges in the input image image and
# marks them in the output map edges

threshold1 = 50
threshold2 = 150
edged = cv2.Canny(edge_img, threshold1, threshold2)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# find contours in the edge map
cnts, h = cv2.findContours(edged.copy(),
                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

max_contA = cv2.contourArea(cnts[0])
max_cont = max(cnts, key=cv2.contourArea)

for i in range(len(cnts)):
    x, y, w, h = cv2.boundingRect(max_cont)
    cv2.rectangle(edge_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
croppedk = frame[y:y + h, x:x + w]

# Display the fruit
cv2.imshow('Edges', edge_img)

frame_e = edge_img

# converting BGR to HSV
# hsv = cv2.cvtColor(frame_e, cv2.COLOR_BGR2HSV)
# hsv = frame

# define range of red color in HSV
lower_red = np.array([179, 0, 0])
# upper_red = np.array([10, 255, 255])
#
# # create a red HSV colour boundary and
# # threshold HSV image
# redmask1 = cv2.inRange(hsv, lower_red, upper_red)
#
# # define range of red color in HSV
# lower_red = np.array([170, 50, 50])
upper_red = np.array([255, 77, 77])

# create a red HSV colour boundary and
# threshold HSV image
redmask = cv2.inRange(frame_e, lower_red, upper_red)

cv2.imshow('Red_Mask:', redmask)
cnt_r = 0
for r in redmask:
    cnt_r = cnt_r + list(r).count(255)
print("Redness ", cnt_r)

lower_green = np.array([0, 153, 0])
upper_green = np.array([102, 255, 102])
greenmask = cv2.inRange(frame_e, lower_green, upper_green)
cv2.imshow('Green_Mask:', greenmask)
cnt_g = 0
for g in greenmask:
    cnt_g = cnt_g + list(g).count(255)
print("Greenness ", cnt_g)

lower_yellow = np.array([153, 153, 0])
upper_yellow = np.array([255, 255, 0])
yellowmask = cv2.inRange(frame_e, lower_yellow, upper_yellow)
cv2.imshow('Yellow_Mask:', yellowmask)
cnt_y = 0
for y in yellowmask:
    cnt_y = cnt_y + list(y).count(255)
print("Yellowness ", cnt_y)

# Calculate ripeness
tot_area = cnt_r + cnt_y + cnt_g
rperc = cnt_r / tot_area
yperc = cnt_y / tot_area
gperc = cnt_g / tot_area

# Adjust the limits for your fruit
rlimit = 0.3
glimit = 0.5
ylimit = 0.8

if gperc > glimit:
    print("Need time to grow")
elif yperc > ylimit:
    print("Medium Ripeness")
elif rperc > rlimit:
    print("No Ripeness")
else:
    print("Not defined")

# De-allocate any associated memory usage
cv2.waitKey(0)
cv2.destroyAllWindows()
