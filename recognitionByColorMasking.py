import cv2
import pytesseract
import numpy as np


def viewImage(image, name_of_window, wait=0):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(wait)
    cv2.destroyAllWindows()


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

lower = np.array([0, 0, 0])
upper = np.array([180, 255, 70])

# Read image from which text needs to be extracted
img = cv2.imread("sample4.jpg")

# Preprocessing the image starts
color_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(color_image, lower, upper)
viewImage(mask, "mask")

# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))

# Applying dilation on the threshold image
dilation = cv2.dilate(mask, rect_kernel, iterations=1)
viewImage(dilation, "dilation")
# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

im2 = img.copy()

# A text file is created and flushed
file = open("recognized.txt", "w+")
file.write("")
file.close()
for cnt in contours:
    if (1000 <= cv2.contourArea(cnt) <= 1000000):
        x, y, w, h = cv2.boundingRect(cnt)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
        viewImage(cropped, "crop", 400)


        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 255), 2)


        # Open the file in append mode
        file = open("recognized.txt", "a")

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped, lang='rus', config=r'--oem 3 --psm 8')

        # Appending the text into file
        file.write("REC: ")
        file.write(text)
        file.write("\n")
        viewImage(im2, "im_by_iteration", 400)

        # Close the file
        file.close
