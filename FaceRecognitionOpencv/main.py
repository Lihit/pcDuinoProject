#-*- coding:utf-8 -*-
'''
author:wenshao
time:2017-11-3
'''
import numpy as np
from configure import config
from FaceShowGui.FaceShowGui import *
import sys
count = 0

class MyThread(QThread):
    '''
    建立一个线程，用来读取视频，并给GUI发送视频信号
    '''
    updateData = pyqtSignal(np.ndarray)
    flag = 0

    def setFlag(self, revFlag):
        if revFlag is not None:
            self.flag = revFlag

    def run(self):
        global count
        faces = ()
        cascPath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        # print(faceCascade)
        cap = cv2.VideoCapture(1)
        # cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,300)
        # cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,300)
        #cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print('打开视频失败')
            return
        try:
            while True:
                if self.flag == 0:
                    ret, frame = cap.read()
                    # print(frame.shape)
                    count += 1
                    if count % 4 == 0:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        faces = faceCascade.detectMultiScale(
                            gray,
                            scaleFactor=config.HAAR_scaleFactor,
                            minNeighbors=config.HAAR_minNeighbors,
                            minSize=config.HAAR_minSize
                        )
                    # Draw a rectangle around the faces
                    for (x, y, w, h) in faces:
                        cv2.rectangle(
                            frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    if not ret:
                        print('run函数出错')
                        break
                    self.updateData.emit(frame)
                # time.sleep(0.01)
            # else:
            #     time.sleep(1)
        except Exception as e:
            print('MyThread::run出错:')
            print(e)
        finally:
            cap.release()


def main():
    try:
        app = QApplication(sys.argv)
        mywin = MyWindow()
        myth = MyThread()
        myth.updateData.connect(mywin.handleDisplay)
        mywin.stopFlag.connect(myth.setFlag)
        myth.start()
        app.exec_()
    except Exception as e:
        print('main函数出错')
        print(e)


if __name__ == '__main__':
    main()
