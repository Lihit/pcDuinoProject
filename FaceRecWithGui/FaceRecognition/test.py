# coding=utf-8
import face_recognition as fr
import cv2
import os


def main1():
    '''
    人脸检测测试
    '''
    img = fr.load_image_file('images/friends_min.jpg')
    face_locations = fr.face_locations(img)

    print(face_locations)
    # 用opencv来显示人脸
    img = cv2.imread("images/friends_min.jpg")
    cv2.namedWindow("origin img")
    cv2.imshow("origin img", img)

    # 遍历人脸，并标注
    faceNum = len(face_locations)
    for i in range(faceNum):
        top = face_locations[i][0]
        right = face_locations[i][1]
        bottom = face_locations[i][2]
        left = face_locations[i][3]
        cv2.rectangle(img, (left, top), (right, bottom), (255, 255, 0), 1)

    # 显示检测结果
    cv2.namedWindow("detected img")
    cv2.imshow("detected img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main2():
    '''
    人脸识别测试
    '''
    unknown_img = None
    known_encoding = None
    img = None
    currentPath = os.getcwd()
    known_imgs = []
    known_labels = []
    imagesPath = os.path.join(currentPath, 'images')
    for filename in os.listdir(imagesPath):
        filepath = os.path.join(imagesPath, filename)
        print(filepath)
        # image=cv2.imread(filepath)
        # cv2.imwrite(filepath,cv2.resize(image,(224,224)))
        if filename == 'unknown.jpg':
            img = cv2.imread(filepath)
            unknown_img = fr.load_image_file(filepath)
            unknown_encoding = fr.face_encodings(unknown_img)[0]
            continue
        known_img = fr.load_image_file(filepath)
        known_encoding = fr.face_encodings(known_img)[0]
        known_imgs.append(known_encoding)
        known_labels.append(filename.split('.')[0])
    results = fr.compare_faces(known_imgs, unknown_encoding)
    print('results:' + str(results))
    name = 'unknown'
    for i in range(len(results)):
        if results[i]:
            name = known_labels[i]
            print('The person is:' + known_labels[i])
            break
    knownface_location = fr.face_locations(unknown_img)
    top = knownface_location[0][0]
    right = knownface_location[0][1]
    bottom = knownface_location[0][2]
    left = knownface_location[0][3]
    cv2.rectangle(img, (left, top), (right, bottom), (255, 255, 0), 1)
    cv2.rectangle(img, (left, bottom), (right, min(
        bottom + 50, img.shape[0])), (255, 255, 0), 1)
    cv2.putText(img, name, (left + 30, bottom + 30),
                cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("detect image", img)
    cv2.waitKey(0)


def main3():
    jobs_image = cv2.imread("images_test/obama.jpg")
    print(type(jobs_image))
    obama_image = fr.load_image_file("images_test/biden.jpg")
    unknown_image = fr.load_image_file("images_test/unknown.jpg")

    jobs_encoding = fr.face_encodings(jobs_image)[0]
    obama_encoding = fr.face_encodings(obama_image)[0]
    unknown_encoding = fr.face_encodings(unknown_image)[0]

    results = fr.compare_faces(
        [jobs_encoding, obama_encoding], unknown_encoding)
    labels = ['obama', 'biden']

    print('results:' + str(results))

    for i in range(0, len(results)):
        if results[i]:
            print('The person is:' + labels[i])


def main4():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600)
    while(1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imshow("capture", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main3()
