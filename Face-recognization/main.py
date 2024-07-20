# import the necessary packages
import cv2

face_detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_dectector = cv2.CascadeClassifier('haarcascade_eye.xml')

image = cv2.imread('tomato.jpg')
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

results = face_detector.detectMultiScale(gray_img, scaleFactor=1.15,minNeighbors=5,minSize=(34, 35), flags=cv2.CASCADE_SCALE_IMAGE)
print(results)

