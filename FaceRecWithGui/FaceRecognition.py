import face_recognition as fr
import cv2
import os

def RecogniseFace(faceInput):
    '''
    用来检测人脸，将输入的人脸与KnownFaces做比对
    :param faceInput: 输入要识别的人脸
    :return: (ret,nameResult,faceOutput) 
    ret是判断是否检测到人脸
    nameResult返回识别出来的名字，如果没识别出来就是Unknown
    faceOutput是faceInput标记人脸位置和名字后生成的图片
    '''
    if faceInput is None:
        return None
    ret=False
    faceOutput=faceInput.copy()
    unknown_encoding=fr.face_encodings(faceOutput)[0]
    currentPath = os.getcwd()
    nameResult='Unknown'
    imagesPath = os.path.join(currentPath, 'KnownFaces')
    for filename in os.listdir(imagesPath):
        filepath = os.path.join(imagesPath, filename)
        known_img = fr.load_image_file(filepath)
        known_encoding = fr.face_encodings(known_img)[0]
        results=fr.compare_faces([known_encoding],unknown_encoding)
        if results[0]==True:
            nameResult=filename.split('.')[0]
            ret=True
            break

    knownface_location = fr.face_locations(faceOutput)
    top = knownface_location[0][0]
    right = knownface_location[0][1]
    bottom = knownface_location[0][2]
    left = knownface_location[0][3]
    cv2.rectangle(faceOutput, (left, top), (right, bottom), (255, 255, 0), 1)
    cv2.rectangle(faceOutput, (left, bottom), (right, min(bottom + 50, faceOutput.shape[0])), (255, 255, 0), 1)
    cv2.putText(faceOutput, nameResult, (left + 30, bottom + 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
    return (ret,nameResult,faceOutput)

def saveNewFace(newFace,newName):
    '''
    用来保存新的人脸到KnownFaces文件夹里
    :param newFace: 新的人脸
           newName: 新的姓名
    :return: ret bool如果保存成功则返回True
    '''
    ret=False
    if newFace is not None:
        currentPath = os.getcwd()
        try:
            cv2.imwrite(os.path.join(currentPath,'KnownFaces',newName)+'.jpg',newFace)
            ret=True
        except Exception as e:
            print(e)
            ret=False
    return ret

if __name__=="__main__":
    print('hello')
    faceInput=cv2.imread('images_test/unknown1.jpg')
    saveNewFace(faceInput,'obamanew')
    (ret, nameResult, faceOutput)=RecogniseFace(faceInput)
    cv2.imshow('recoImg',faceOutput)
    cv2.waitKey(0)
    cv2.destroyAllWindows()