import cv2
import pytesseract
import numpy as np
import os.path
import sys
import shutil


def viewImage(image, name_of_window, wait=0):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(wait)
    cv2.destroyAllWindows()


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

num_img = 1
name_file = "AllTrainData.txt"
name_copy_file = "OCRTrainData.txt"
lower = np.array([0, 0, 0])
upper = np.array([180, 255, 70])

print("Checking for any images named \"sample<#>.jpg\"...\n")

# A text file is created and flushed
try:
    with open(name_file, "w+") as file:
        print("Succesfully opened txt-file!\n")
        file.write("Version 1.0.0\n")
except IOError:
    print("Error opening txt-file!\n")

name_img = "sample" + str(num_img) + ".jpg"

print("Scanning images...\n")

while os.path.isfile(name_img):


    # Read image from which text needs to be extracted
    img = cv2.imread(name_img)

    print(name_img)
    # print(img.shape)

    # Preprocessing the image starts
    color_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(color_image, lower, upper)
    # viewImage(mask, "mask")

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(mask, rect_kernel, iterations=1)
    # viewImage(dilation, "dilation")
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    im2 = img.copy()


    counter = 0
    out = " "

    for cnt in contours:
        if (1000 <= cv2.contourArea(cnt) <= 700000):
            x, y, w, h = cv2.boundingRect(cnt)
            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]
            # viewImage(cropped, "crop", 400)

            # Drawing a rectangle on copied image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 255), 2)

            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped, lang='rus', config=r'--oem 3 --psm 8')
            print(text)
            if text.find("Дата сортировки") >= 0 or text.find("ата сорт") >= 0 or text.find("та сор") >= 0 or text.find("та со") >= 0 or text.find("Дата") >= 0 or text.find("дата") >= 0 or text.find("дат") >= 0 or text.find("Дат") >= 0:
                counter = counter + 1
                out = out + "R:4 " + str(x) + " " + str(y) + " " + str(x + w) + " " + str(y) + " " + str(
                    x + w) + \
                      " " + str(y+h) + " " + str(x) + " " + str(y+h) + \
                      " 0 \"Datacoptipovki\" "

            if text.find("Годен") >= 0 or text.find("годен") >= 0 or text.find("до") >= 0 or text.find("годен до") >= 0 or text.find("Годен до") >= 0 or text.find("Год") >= 0 or text.find("ен до") >= 0 or text.find("год") >= 0:
                counter = counter + 1
                out = out + "R:4 " + str(x) + " " + str(y) + " " + str(x + w) + " " + str(y) + " " + str(
                    x + w) + \
                      " " + str(y+h) + " " + str(x) + " " + str(y+h) + \
                      " 0 \"Godendo\" "

            if text.find("(ЛИ)") >= 0 or text.find("И)") >= 0 or text.find("(Л") >= 0:
                counter = counter + 1
                out = out + "R:4 " + str(x) + " " + str(y) + " " + str(x + w) + " " + str(y) + " " + str(
                    x + w) + \
                      " " + str(y+h) + " " + str(x) + " " + str(y+h) + \
                      " 0 \"(LI)\" "

            if text.find("(ДА)") >= 0 or text.find("(Д") >= 0 or text.find("А)") >= 0:
                counter = counter + 1
                out = out + "R:4 " + str(x) + " " + str(y) + " " + str(x + w) + " " + str(y) + " " + str(
                    x + w) + \
                      " " + str(y+h) + " " + str(x) + " " + str(y+h) + \
                      " 0 \"(DA)\" "

            if text.find("(ОК)") >= 0 or text.find("(О") >= 0 or text.find("К)") >= 0:
                counter = counter + 1
                out = out + "R:4 " + str(x) + " " + str(y) + " " + str(x + w) + " " + str(y) + " " + str(
                    x + w) + \
                      " " + str(y+h) + " " + str(x) + " " + str(y+h) + \
                      " 0 \"(OK)\" "

    # viewImage(im2, name_img)
    file = open(name_file, "a")
    file.write(name_img + ":" + str(counter) + out + "\n")
    file.close()

    num_img = num_img + 1
    name_img = "sample" + str(num_img) + ".jpg"

shutil.copyfile(name_file, name_copy_file)
print("\nScanned successfully, check the txt-file")
print("Exiting the program...")
sys.exit(0)
