import cv2 
import numpy as np
from colour import delta_E
import os

AREA_WINNAME = "Select Text Area"
COLOR_WINNAME = "Select Text Color"
FINAL_WINNAME = "Text Only"
DELTA_E_TOLERANCE = 15.0

colorCords = []
kek = []

def colorPickerEvent(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global colorCords 
        colorCords = [y,x]
        cv2.destroyWindow(COLOR_WINNAME)
    # if event == cv2.EVENT_MOUSEMOVE:
    #     colorsBGR = kek[y,x]
    #     colorsRGB=tuple(reversed(colorsBGR))
    #     print("RGB Value at ({},{}):{} ".format(x,y,colorsRGB))

def getTextArea(imagePath):
    image = cv2.imread(imagePath)
    textArea = cv2.selectROI(AREA_WINNAME, image)
    return image[textArea[1]:textArea[1]+textArea[3], textArea[0]:textArea[0]+textArea[2]]

def getTextColor(textArea):
    cv2.namedWindow(COLOR_WINNAME)
    cv2.setMouseCallback(COLOR_WINNAME, colorPickerEvent)
    cv2.imshow(COLOR_WINNAME, textArea)
    while cv2.getWindowProperty(COLOR_WINNAME,0) >=0:
        cv2.waitKey(100)
    return np.array(textArea[colorCords[0]:colorCords[0]+1,colorCords[1]:colorCords[1]+1])

def getTextImage(textArea, colorPixel=np.zeros(shape=(1,1,3), dtype=np.int32), isColorFilterNeeded=True):
    if not isColorFilterNeeded:
        return cv2.cvtColor(textArea, cv2.COLOR_BGR2GRAY)
    for pixelColorIndex in np.ndindex(textArea.shape[:2]):
        labA = cv2.cvtColor(np.expand_dims(textArea[pixelColorIndex],axis =(0,1)),cv2.COLOR_BGR2LAB)
        labB = cv2.cvtColor(colorPixel,cv2.COLOR_BGR2LAB)
        dltE = delta_E(labA[0,0], labB[0,0])
        if dltE > DELTA_E_TOLERANCE:
            textArea[pixelColorIndex] = np.full(shape=(3),fill_value=255,dtype=np.int32)
        else:
            textArea[pixelColorIndex] = np.zeros(shape=(3),dtype=np.int32)
    return cv2.cvtColor(textArea, cv2.COLOR_BGR2GRAY)

def getFinalText(imgPath):
    area = getTextArea(imgPath)
    cv2.destroyWindow(AREA_WINNAME)
    global kek
    kek = area
    print("Color filter need?\n")
    inp = input("N/Н for skip = ")
    if inp.lower() in "н n":
        return getTextImage(area,isColorFilterNeeded=False)
    color = getTextColor(area)
    final = getTextImage(area,color)
    return final

def testFunc():
    imgPath = "test3.jpeg"
    text = getFinalText(imgPath)
    cv2.imshow("f", text)
    ocr(text)
    cv2.waitKey(0)

def ocr(textImage):
    way = r"D:\Projects\Python\vscode\Images\temp.jpg"
    cv2.imwrite(way, textImage)
    cmd='tesseract {0} out -l jpn_vert'.format(way)
    txt = os.popen(cmd).read()
    try:
        os.remove(way)
    except:
        pass

testFunc()