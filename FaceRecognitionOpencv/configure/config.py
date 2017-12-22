import os
#coding=utf-8

BASE_DIR=os.path.abspath('./')
FACES_DIR=os.path.join(BASE_DIR,'FaceRecognition','KnownFaces')
MODEL_DIR=os.path.join(BASE_DIR,'FaceRecognition','model')
MODEL_FILENAME='mymodel.xml'
MODEL_PATH=os.path.join(MODEL_DIR,MODEL_FILENAME)
HAARFILE_PATH=os.path.join(BASE_DIR,'haarcascade_frontalface_default.xml')
HAAR_scaleFactor=1.1
HAAR_minNeighbors=5
HAAR_minSize=(150, 150)
FACE_WIDTH  = 150
FACE_HEIGHT = 150
IP=''
PORT=8899

