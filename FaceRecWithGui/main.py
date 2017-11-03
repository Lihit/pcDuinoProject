import cv2
import skvideo.io
import time
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from FaceRecWithGui.FaceRecognition.FaceRecognition import *
from FaceRecWithGui.FaceShowGui.FaceShowGui import *


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
        cap = skvideo.io.VideoCapture('1.mp4')
        if not cap.isOpened():
            print('打开视频失败')
            return
        try:
            while True:
                if self.flag == 0:
                    ret, frame = cap.read()
                    if not ret:
                        print('run函数出错')
                        break
                    self.updateData.emit(frame)
                    # time.sleep(0.04)
                # else:
                #     time.sleep(1)
        except Exception as e:
            print('MyThread::run出错:')
            print(e)


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
