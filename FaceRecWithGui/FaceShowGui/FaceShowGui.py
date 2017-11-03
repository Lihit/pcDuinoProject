# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
import sys
import numpy as np
import face_recognition as fr
import cv2
from FaceRecWithGui.FaceRecognition.FaceRecognition import saveNewFace

class MyWindow(QWidget):
    def __init__(self, WinWidth=800, WinHeight=600):
        '''
        搭建一个GUI病初始化
        :param WinWidth: 窗口的宽
        :param WinHeight: 窗口的高
        '''
        super().__init__()
        self.count = 0
        self.face_locations = None
        self.WinWidth = WinWidth
        self.WinHeight = WinHeight
        self.currentFrame = None
        self.newName = None
        self.initUI()

    def initUI(self):
        '''
        布局设置和控件设置
        :return: QThread
        
        '''
        self.recoBtn = QPushButton('开始识别', self)
        self.inBtn = QPushButton('录入人脸', self)
        self.recoBtn.clicked.connect(self.clickEvent)
        self.inBtn.clicked.connect(self.clickEvent)
        self.scene = QGraphicsScene()
        self.item = QGraphicsPixmapItem()
        self.scene.addItem(self.item)
        self.graphicsview = QGraphicsView()
        self.graphicsview.setScene(self.scene)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.graphicsview)
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.recoBtn)
        hbox.addWidget(self.inBtn)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # 窗口设置
        self.resize(self.WinWidth, self.WinHeight)
        self.setWindowTitle("FaceRecognition")
        self.center()
        self.show()

    def clickEvent(self):
        '''
        按下按钮的对话框
        :return: 
        '''
        #text, ok = QInputDialog.getText(self, '输入对话框', '请输入你的名字:')
        source = self.sender()
        if source.text() == '录入人脸':
            text, ok = QInputDialog.getText(self, '输入对话框', '请输入你的名字:')
            if ok:
                self.newName=text
                ret=saveNewFace(self.currentFrame,self.newName)
                if ret:
                    reply = QMessageBox.question(self, 'Info', '人脸录入成功',QMessageBox.Yes )
                else:
                    reply = QMessageBox.question(self, 'Warning', '人脸录入失败，请重新录入！', QMessageBox.Yes)
        elif source.text() == '开始识别':
            pass

    def DetectFace(self, frame):
        face_locations = fr.face_locations(frame)
        return face_locations

    def DrawFaces(self, frame, face_locations):
        if face_locations is None:
            return frame
        faceNum = len(face_locations)
        for i in range(faceNum):
            top = face_locations[i][0]
            right = face_locations[i][1]
            bottom = face_locations[i][2]
            left = face_locations[i][3]
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 1)
        return frame

    def handleDisplay(self, frame):
        if len(frame):
            self.count += 1
            self.currentFrame=frame.copy()
            # frame=np.array(frame,dtype=np.uint8)
            if self.count % 3 == 0:
                self.face_locations = self.DetectFace(frame)
            frame = self.DrawFaces(frame, self.face_locations)
            height, width, bytesPerComponent = frame.shape
            self.resize(width + 40, height + 70)
            bytesPerLine = 3 * width
            QImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.item.setPixmap(QPixmap.fromImage(QImg))

    def center(self):
        '''
        将窗口放在屏幕的中心
        :return: 
        '''
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MyWindow()
    app.exec_()
