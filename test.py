import cv2
import numpy as np
from colour import delta_E

clickedColorLAB = None
def colorPicker(event, x, y, flags, param):
    global clickedColorLAB
    if event == cv2.EVENT_LBUTTONDOWN:
        colorsBGR = first[y:y+1,x:x+1]
        labim = cv2.cvtColor(colorsBGR,cv2.COLOR_BGR2LAB)
        clickedColorLAB = labim[0,0]
        print("New base {} Lab".format(clickedColorLAB))
    if event == cv2.EVENT_RBUTTONDOWN:
        colorsBGR2 = first[y:y+1,x:x+1]
        labim2 = cv2.cvtColor(colorsBGR2,cv2.COLOR_BGR2LAB)
        toval = labim2[0,0]
        print("To compare {} Lab".format(toval))
        dlt = delta_E(clickedColorLAB,toval)
        print("Delta E = {}".format(dlt))


img = cv2.imread("test2.jpg")
roi = cv2.selectROI("Region", img)
r = roi
first = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]
cv2.namedWindow("test")
cv2.setMouseCallback("test",colorPicker)
cv2.imshow("test",first)
cv2.waitKey(0)