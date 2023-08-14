import cv2
import pytesseract


def viewImage(image, name_of_window, wait=0):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(wait)
    cv2.destroyAllWindows()


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Read image from which text needs to be extracted
img = cv2.imread("sample2.jpg")

# Preprocessing the image starts

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
viewImage(gray, "gray")
# Performing OTSU threshold
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
viewImage(thresh1, "threshold")

# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 35))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
viewImage(dilation, "dilation")

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# for contour in contours

im2 = gray.copy()

# A text file is created and flushed
file = open("recognized.txt", "w+")
file.write("")
file.close()
for cnt in contours:
    if (5000 <= cv2.contourArea(cnt) <= 1000000):
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 255), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
        viewImage(cropped, "crop", 400)

        # Open the file in append mode
        file = open("recognized.txt", "a")

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped, lang='rus', config=r'--oem 3 --psm 6')

        # Appending the text into file
        file.write(text)
        file.write("\n")
        viewImage(im2, "im_by_iteration", 400)

        # Close the file
        file.close
# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
#text = pytesseract.image_to_string(dilation, lang='rus', config=r'--oem 3 --psm 6')
#file = open("recognized.txt", "a")
#file.write(text)
#file.write("\n")
#file.close
#viewImage(im2, "im_by_iteration")
