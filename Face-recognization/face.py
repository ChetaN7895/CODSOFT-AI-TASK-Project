import sys
import time
import os
import numpy as np
from PIL import Image
import cv2
path = 'user_data'
name =''
if not os.path.exists("user_data"):
    os.mkdir('user_data')
    # print("Directory " , dirName ,  " Created ")

def face_generator():
    global name
    cam = cv2.VideoCapture(0)#used to create video which is used to capture images
    cam.set(3,640)
    cam.set(4,480)
    dectector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # this file is used to detect a object in an image
    face_id=input("enter id of user :")
    name=input("enter name :")
    sample=int(input("Enter how many sample you wish to take  : "))

    for f in os.listdir(path): #remove old images from user data folder if present
        os.remove(os.path.join(path, f))
    print("taking sample image of user ...please look at camera")
    time.sleep(20)

    count=0
    while True:
        ret,img=cam.read()# read the frames using above created objects
        converted_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#converts image to black and white
        faces=dectector.detectMultiScale(converted_image,1.3,5)#detect face in image

        for (x,y,w,h) in faces:
            
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)#creates frame around face
            count+=1
            # print(count)

            cv2.imwrite("user_data/face."+str(face_id)+"."+str(count)+".jpg",converted_image[y:y+h,x:x+w])
            # To caputure image and save in user_data folder

            cv2.imshow("image",img)#displays image on window

        k=cv2.waitKey(1) & 0xff
        if k==27:
            break
        elif count>=sample:
            break
    print("Image Samples taken succefully !!!!.")
    cam.release()
    cv2.destroyAllWindows()

def traning_data():
    # used to recognize faces in images and videos
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    #creates an instance of a face detection classifier using the Haar Cascade classifier
    #pre-trained model for detecting faces in images
    dectector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 

    def Images_And_Labels(path):
        imagesPaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []

        for imagePath in imagesPaths:
            gray_image = Image.open(imagePath).convert('L')  # convert to grayscale
            img_arr = np.array(gray_image, 'uint8')  # creating array

            # extracts the label (id) from the image file name
            id = int(os.path.split(imagePath)[-1].split(".")[1])

            # detects faces in the image using the face detection classifier
            faces = dectector.detectMultiScale(img_arr)

            for (x, y, w, h) in faces:
                faceSamples.append(img_arr[y:y + h, x:x + w])
                ids.append(id)
        return faceSamples, ids

    print("Training Data...please wait...!!!")
    faces, ids = Images_And_Labels(path)

    # trains the face recognizer using the loaded face data (faces) and labels (ids).
    recognizer.train(faces, np.array(ids))
    # saves the trained recognizer to a YAML file called 'trained_data.yml'.
    recognizer.write('trained_data.yml') 

    print("data Trained successfully !!!!")

def detection():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trained_data.yml')  # loaded trained model
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX  # denotes fonts size

    id = 5  # number of persons your want to recognize
    names = ['',name]
    cam = cv2.VideoCapture(0)  # used to create video which is used to capture images
    cam.set(3, 640)
    cam.set(4, 480)

    # define min window size to be recognize as a face
    minW = 0.1 * cam.get(3)
    maxW = 0.1 * cam.get(4)
    no = 0
    while True:
        if cam is None or not cam.isOpened():
            print('Warning: unable to open video source: ')

        ret, img = cam.read()  # read the frames using above created objects
        if ret == False:
            print("unable to detect img")
        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # converts image to black and white

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minW)),
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            id, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])
            # check if accuracy is less than 100 ==> "0" is perfect match
            # print(accuracy)
            if (accuracy < 100):
                id = names[id]
                accuracy = " {0}%".format(round(100 - accuracy))
                # print(no)
                no += 1
            else:
                id = "unknown"
                accuracy = " {0}%".format(round(100 - accuracy))
                # print(no)
                no += 1
            cv2.putText(img, "press Esc to close this window", (5, 25), font, 1, (255, 0, 255), 2)
            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 0, 255), 2)
            cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
        cv2.imshow('camera', img)
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

def permisssion(val,task):
    if "Y"==val or "y" ==val:
         if task == 1:
             traning_data()
         elif task == 2:
             detection()
    else:
        print("ThankYou for using this application !! ")
        sys.exit()


print("\t\t\t ##### Welcome to face Authentication System #####")
face_generator()
perm=input("Do you wish to train your image data for face authentication [y|n] : ")
permisssion(perm,1)
authenticate=input("Do your want test authentication system [y|n] : ")
permisssion(authenticate,2)

