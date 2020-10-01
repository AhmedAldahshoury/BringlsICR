import tensorflow as tf
import cv2
import numpy as np
from scipy import ndimage
import sys
import os


def getBestShift(img):
    cy, cx = ndimage.measurements.center_of_mass(img)
    rows, cols = img.shape
    shiftx = np.round(cols / 2.0 - cx).astype(int)
    shifty = np.round(rows / 2.0 - cy).astype(int)
    return shiftx, shifty


def shift(img, sx, sy):
    rows, cols = img.shape
    M = np.float32([[1, 0, sx], [0, 1, sy]])
    shifted = cv2.warpAffine(img, M, (cols, rows))
    return shifted


if len(sys.argv) > 1:
    image = sys.argv[1]
else:
    print(
        "Usage --> python segmentation.py <ImgName> --optional<inverted?> --optional<height> --optional<width> --optional<pad size> ")
    print("example  --> python segmentation.py <testImage> 40 100 20 true")
    exit(1)

if not os.path.exists("../dataset/raw/" + image + ".png"):
    print("File : " + image + ".png doesn't exist")
    exit(1)

# read original image
color_complete = cv2.imread("../dataset/raw/" + image + ".png")
print(("reading: " + str(image) + ".png"))

# read the grayscale image
if (len(color_complete.shape) < 3):
    gray_complete = color_complete
    print("Image selected is already grayscale !!")
elif len(color_complete.shape) == 3:
    gray_complete = cv2.cvtColor(color_complete, cv2.COLOR_BGR2GRAY)

# gray_complete = cv2.cvtColor(color_complete,cv2.COLOR_BGR2GRAY)
recognized_complete = color_complete
invert = False

if (len(sys.argv) > 3):
    dheight = int(sys.argv[3])
else:
    dheight = gray_complete.shape[0]
if (len(sys.argv) > 4):
    dwidth = int(sys.argv[4])
else:
    dwidth = gray_complete.shape[1]
if (len(sys.argv) > 5):
    dpad = int(sys.argv[5])
else:
    dpad = 30
if (len(sys.argv) > 2):
    if (int(sys.argv[2]) == 1):
        invert = True
    else:
        invert = False

img_row_sum = np.sum(gray_complete, axis=1).tolist()

gray_complete = cv2.adaptiveThreshold(gray_complete, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 171, 90)
_, gray_complete = cv2.threshold(gray_complete, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
ret, gray_complete_inv = cv2.threshold(gray_complete, 0, 255, cv2.THRESH_BINARY_INV)

# if not os.path.exists("../dataset/segmented/" + image):
#   os.makedirs("../dataset/segmented/" + image)
if not os.path.exists("../dataset/segmented"):
    os.makedirs("../dataset/segmented")
if not os.path.exists("../dataset/rawGS"):
    os.makedirs("../dataset/rawGS")
# cv2.imwrite("../dataset/results/"+image+"/"+image+"_grayscale.png", gray_complete)

height, width = gray_complete.shape
cnts, _ = cv2.findContours(gray_complete_inv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
avgCntArea = np.mean([cv2.contourArea(k) for k in cnts])
if (invert):
    print("Images will be inverted !!")

cv2.imwrite("../dataset/rawGS/" + image + "_GrayScale.png", gray_complete)

id = 0

for (i, c) in enumerate(cnts):

    if cv2.contourArea(c) < avgCntArea / 10:
        continue
    mask = np.zeros(gray_complete_inv.shape, dtype="uint8")
    (x, y, w, h) = cv2.boundingRect(c)
    digit = gray_complete_inv[y:y + h, x:x + w]
    segmented = gray_complete_inv[y:y + h, x:x + w]
    segmented = np.lib.pad(segmented, ((dpad, dpad), (dpad, dpad)), 'constant')
    ret, segmented = cv2.threshold(segmented, 0, 255, cv2.THRESH_BINARY_INV)
    height, width = digit.shape[:2]

    if width > 1 and height > 1:
        id += 1
        rows, cols = digit.shape
        compl_dif = abs(rows - cols)
        half_Sm = int(compl_dif / 2)
        half_Big = half_Sm if half_Sm * 2 == compl_dif else half_Sm + 1
        if rows > cols:
            digit = np.lib.pad(digit, ((0, 0), (half_Sm, half_Big)), 'constant')
        else:
            digit = np.lib.pad(digit, ((half_Sm, half_Big), (0, 0)), 'constant')
        resizeValue = min(dheight, dwidth)
        resizeValue = resizeValue - (dpad * 2)
        if (resizeValue < 1):
            print("choose smaller padding value !!")
            exit(1)
        digit = cv2.resize(digit, (resizeValue, resizeValue))
        # cv2.imwrite("../dataset/results/"+image+"/"+image+"_raw_"+str(i)+".png", digit)
        padh = int((dheight - resizeValue) / 2)
        padw = int((dwidth - resizeValue) / 2)
        digit = np.lib.pad(digit, ((padh, padh), (padw, padw)), 'constant')
        shiftx, shifty = getBestShift(digit)
        shifted = shift(digit, shiftx, shifty)
        digit = shifted
        ret, digit = cv2.threshold(digit, 0, 255, cv2.THRESH_BINARY_INV)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(recognized_complete, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(recognized_complete, str(id), (x + int(w / 6), y + h + 20), font, fontScale=0.8, color=(0, 0, 128),
                    thickness=4)
        # cv2.imwrite("results/"+image+"/"+image+"_"+str(i)+".png", digit)
    if (len(sys.argv) > 4):
        if invert:
            ret, digit = cv2.threshold(digit, 0, 255, cv2.THRESH_BINARY_INV)
        #   cv2.imwrite("../dataset/segmented/"+image+"/"+image+"("+str(dheight)+"x"+str(dwidth)+")_"+str(id)+".png", digit)
        cv2.imwrite("static/gallery/" + image + "(" + str(dheight) + "x" + str(dwidth) + ")_" + str(id) + ".png", digit)
    else:
        if invert:
            ret, segmented = cv2.threshold(segmented, 0, 255, cv2.THRESH_BINARY_INV)
        #  cv2.imwrite("../dataset/segmented/"+image+"/"+image+"_"+str(id)+".png", segmented)
        if id < 10:
            cv2.imwrite("static/gallery/" + image + "_00" + str(id) + ".png", segmented)
        else:
            cv2.imwrite("static/gallery/" + image + "_0" + str(id) + ".png", segmented)

cv2.imwrite("../dataset/recognized/recognized.png", recognized_complete)

print("(" + str(image) + ".png) segmented successfully")

# cv2.imwrite("results/digitized_images/"+image+"_digitized_image.png", color_complete)
# cv2.imwrite("results/"+image+"/"+image+"_digitized_image.png", color_complete)
