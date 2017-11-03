# coding=utf-8
import face_recognition as fr
import cv2
import os


def RecogniseFace(faceInput, FacesLabelPredicted=None):
    '''
    用来检测人脸，将输入的人脸与KnownFaces做比对
    :param 
    faceInput: 输入要识别的人脸
    FacesLabelPredicted: 提前预测出来的人脸，可以加快预测速度，这样就不用再遍历一次KnownFaces了
    :return: resultDict 返回一个字典，格式为{position:name},如果识别不到，那么name=unknown
    '''
    resultDict = {}
    if faceInput is None:
        print('传入的图像是None')
        return resultDict
    faceOutput = faceInput.copy()
    '''
    先对输入进来的图像进行人脸检测
    '''
    UnknownFaces_location = fr.face_locations(faceOutput)
    FaceNum = len(UnknownFaces_location)  # 识别出人脸的数目
    if FaceNum == 0:
        print("没有检测出来人脸")
        return resultDict
    UnknownFaces_encoding = fr.face_encodings(faceOutput, UnknownFaces_location)
    '''
    对检测出来的人脸进行识别
    '''
    imagesDir = os.path.join('FaceRecognition', 'KnownFaces')  # 已识别人脸的数据库
    resultDict = {tuple(position): 'unknown' for position in UnknownFaces_location}
    for filename in os.listdir(imagesDir):
        filepath = os.path.join(imagesDir, filename)
        # print(filepath)
        known_img = fr.load_image_file(filepath)
        known_encoding = fr.face_encodings(known_img)[0]
        index_reco = []
        for i in range(len(UnknownFaces_encoding)):
            results = fr.compare_faces([known_encoding], UnknownFaces_encoding[i])
            if results[0] == True:
                resultDict[tuple(UnknownFaces_location[i])] = filename.split('.')[0]
                index_reco.append(i)
        for j in index_reco:
            del UnknownFaces_encoding[j]
            del UnknownFaces_location[j]
        if len(UnknownFaces_encoding) == 0:
            break
    return resultDict


def saveNewFace(faceInput, newName):
    '''
    用来保存新的人脸到KnownFaces文件夹里
    :param newFace: 新的人脸
           newName: 新的姓名
    :return: ret bool如果保存成功则返回True
    '''
    ret = False
    newFace = faceInput.copy()
    if newFace is not None and newName is not None:
        faces_location = fr.face_locations(newFace)
        if len(faces_location) < 1:
            print('没有检测到人脸，请重新录入!')
            return ret
        if len(faces_location) > 1:
            print('检测出来的人脸超过一张,请重新录入!')
            return ret
        imagesDir = 'KnownFaces'
        try:
            top = max(faces_location[0][0] - 20, 0)
            right = min(faces_location[0][1] + 20, newFace.shape[0])
            bottom = min(faces_location[0][2] + 20, newFace.shape[1])
            left = max(faces_location[0][3] - 20, 0)
            # print(os.path.join(imagesDir, newName) + '.jpg')
            # print(type(newFace))
            # print(newFace[top:bottom, left:right])
            face = newFace[top:bottom, left:right]
            (r, g, b) = cv2.split(face)
            face = cv2.merge([b, g, r])
            cv2.imwrite(os.path.join('FaceRecognition', 'KnownFaces', newName) + '.jpg', face)
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
        print('录入成功')
    resultDict = RecogniseFace(faceInput)
    for (top, right, bottom, left) in resultDict.keys():
        cv2.rectangle(faceInput, (left, top), (right, bottom), (255, 255, 0), 1)
        cv2.rectangle(faceInput, (left, bottom), (right, min(bottom + 50, faceInput.shape[0])), (255, 255, 0), 1)
        cv2.putText(faceInput, resultDict[(top, right, bottom, left)], (left + 30, bottom + 30),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('recoImg', faceInput)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
