# -*- coding:utf-8 -*-
'''
author:wenshao
time:2017-11-3
'''
import cv2
import os
import datetime
from configure import config
import numpy as np
import time
import json

model = cv2.createLBPHFaceRecognizer()


def resizeImage(image):
    return cv2.resize(image, (config.FACE_WIDTH, config.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)


def cropImage(image, x, y, w, h):
    return image[y:y + h, x:x + w]


def prepareImage(fileName):
    """Read an image as grayscale and resize it to the appropriate size for
    training the face recognition model.
    """
    image = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    return resizeImage(image)


def train():
    global model
    nameids = {}
    jsonpath = os.path.join(config.FACES_DIR, 'NameMapID.json')
    if os.path.exists(jsonpath):
        with open(jsonpath, 'r') as fp:
            nameids = json.load(fp)
    else:
        print('no json file exist...')
        return
    faces = []
    labels = []
    facesDir = config.FACES_DIR
    persons = os.listdir(facesDir)
    for person in persons:
        if person.find('.json') != -1:
            continue
        personDir = os.path.join(facesDir, person)
        for filename in os.listdir(personDir):
            faces.append(prepareImage(os.path.join(personDir, filename)))
            labels.append(nameids[person])
    # Start training model
    model.train(np.asarray(faces), np.asarray(labels))
    # Save model results
    model.save(config.MODEL_PATH)
    print('sucessfully train the model...')


def RecogniseFace(faceInput):
    '''
    用来检测人脸，将输入的人脸与KnownFaces做比对
    :param 
    faceInput: 输入要识别的人脸
    FacesLabelPredicted: 提前预测出来的人脸，可以加快预测速度，这样就不用再遍历一次KnownFaces了
    :return: resultDict 返回一个字典，格式为{position:name},如果识别不到，那么name=unknown
    '''
    global model
    nameids = {}
    jsonpath = os.path.join(config.FACES_DIR, 'NameMapID.json')
    if os.path.exists(jsonpath):
        with open(jsonpath, 'r') as fp:
            nameids = json.load(fp)
    else:
        print('no json file exist...')
        return
    nameids_reverse = {value: key for key, value in nameids.items()}
    image = faceInput.copy()
    resultDict = {}
    modelPath = config.MODEL_PATH
    if not os.path.exists(modelPath):
        train()
    model.load(modelPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(config.HAARFILE_PATH)
    faces_location = faceCascade.detectMultiScale(
        gray,
        scaleFactor=config.HAAR_scaleFactor,
        minNeighbors=config.HAAR_minNeighbors,
        minSize=config.HAAR_minSize
    )
    resultDict = {tuple(position): 'unknown' for position in faces_location}
    # print(resultDict)
    for face in faces_location:
        img_crop = cropImage(gray, *face)
        img_resize = resizeImage(img_crop)
        # print(type(img_crop))
        label, confidence = model.predict(img_resize)
        print(nameids_reverse[label] + ' confidence:' + str(confidence))
        if confidence<=45:
            if label in nameids_reverse.keys():
                resultDict[tuple(face)] = nameids_reverse[label]
        else:
            print('the confidence is too big,it is not correct!')
    return resultDict


def saveNewFace(faceInput, newName):
    '''
    用来保存新的人脸到KnownFaces文件夹里
    :param newFace: 新的人脸
           newName: 新的姓名
    :return: ret bool如果保存成功则返回True
    '''
    time_str = str(time.time()).replace('.', '')
    ret = False
    newFace = faceInput.copy()
    [b, g, r] = cv2.split(newFace)
    newFace = cv2.merge([r, g, b])
    faceCascade = cv2.CascadeClassifier(config.HAARFILE_PATH)
    if newFace is not None and newName is not None:
        gray = cv2.cvtColor(newFace, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=config.HAAR_scaleFactor,
            minNeighbors=config.HAAR_minNeighbors,
            minSize=config.HAAR_minSize
        )
        if len(faces) < 1:
            print(u'没有检测到人脸，请重新录入!')
            return ret
        if len(faces) > 1:
            print(u'检测出来的人脸超过一张,请重新录入!')
            return ret
        try:
            (x, y, w, h) = faces[0]
            face = newFace[y:y + h, x:x + w]
            newFaceDir = os.path.join(config.FACES_DIR, newName)
            if not os.path.exists(newFaceDir):
                os.mkdir(newFaceDir)
            cv2.imwrite(os.path.join(newFaceDir, time_str + '.jpg'), face)
            nameids = {}
            jsonpath = os.path.join(config.FACES_DIR, 'NameMapID.json')
            if os.path.exists(jsonpath):
                with open(jsonpath, 'r') as fp:
                    nameids = json.load(fp)
            if not newName in nameids.keys():
                nameids[newName] = len(nameids)
            with open(jsonpath, 'w') as fp:
                json.dump(nameids, fp)
            ret = True
        except Exception as e:
            print(e)
            ret = False
    return ret


if __name__ == "__main__":
    print('hello')
    faceInput = cv2.imread('images_test/friend.jpg')
    ret = saveNewFace(faceInput, 'obama_new')
    if ret:
        print(u'录入成功')
    resultDict = RecogniseFace(faceInput)
    for (top, right, bottom, left) in resultDict.keys():
        cv2.rectangle(faceInput, (left, top),
                      (right, bottom), (255, 255, 0), 1)
        cv2.rectangle(faceInput, (left, bottom), (right, min(
            bottom + 50, faceInput.shape[0])), (255, 255, 0), 1)
        cv2.putText(faceInput, resultDict[(top, right, bottom, left)], (left + 30, bottom + 30),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('recoImg', faceInput)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
