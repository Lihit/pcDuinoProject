# -*- coding:utf-8 -*-
'''
author:wenshao
time:2017-11-3
'''
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import *
import cv2
from FaceRecognition.FaceRecognition import saveNewFace, RecogniseFace, train
from socket import *
import json
from datetime import datetime
from configure import config


class MyWindow(QWidget):
    stopFlag = pyqtSignal(int)

    def __init__(self, WinWidth=800, WinHeight=600):
        '''
        搭建一个GUI病初始化
        :param WinWidth: 窗口的宽
        :param WinHeight: 窗口的高
        '''
        super(QWidget, self).__init__()
        train()
        self.count = 0
        self.face_locations = None
        self.WinWidth = WinWidth
        self.WinHeight = WinHeight
        self.currentFrame = None
        self.newName = None
        # 建立一个udp套接字，建识别出来的人脸发送到服务器
        self.dstIP = config.IP
        self.dstPort = config.PORT
        self.UdpSocket = socket(AF_INET, SOCK_DGRAM)
        self.initUI()

    def initUI(self):
        '''
        布局设置和控件设置
        :return: QThread

        '''
        self.recoBtn = QPushButton('开始识别', self)
        self.inBtn = QPushButton('录入人脸', self)
        self.snapshotBtn = QPushButton('拍照', self)
        self.stopBtn = QPushButton('暂停', self)
        self.recoBtn.clicked.connect(self.clickEvent)
        self.inBtn.clicked.connect(self.clickEvent)
        self.snapshotBtn.clicked.connect(self.clickEvent)
        self.stopBtn.clicked.connect(self.clickEvent)
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
        hbox.addWidget(self.snapshotBtn)
        hbox.addWidget(self.stopBtn)
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
        '''
        source = self.sender()
        if source.text() == u'录入人脸':
            text, ok = QInputDialog.getText(self, '输入对话框', '请输入你的名字:')
            if ok:
                self.newName = text
                ret = saveNewFace(self.currentFrame, self.newName)
                if ret:
                    reply = QMessageBox.question(
                        self, 'Info', '人脸录入成功', QMessageBox.Yes)
                    send_json = json.dumps(
                        [0, self.newName, str(datetime.now())])
                    print('input face:' + send_json)
                    self.UdpSocket.sendto(send_json.encode(
                        'utf-8'), (self.dstIP, self.dstPort))
                    print('Retrain the model...')
                    train()
                else:
                    reply = QMessageBox.question(
                        self, 'Warning', '人脸录入失败，请重新录入！', QMessageBox.Yes)
        elif source.text() == u'开始识别':
            resultDict = RecogniseFace(self.currentFrame)
            recoNames = []
            sendList = []
            for key, value in resultDict.items():
                if value == 'unknown':
                    continue
                (top, right, bottom, left) = key
                sendList.append([1, value, str(datetime.now())])  # 1代表的是识别
                recoNames.append(value)
            if len(recoNames) == 0:
                reply = QMessageBox.question(
                    self, 'Warning', '无法识别人脸，请重新识别！', QMessageBox.Yes)
            else:
                sendList_json = json.dumps(sendList)
                print('reco face:' + sendList_json)
                self.UdpSocket.sendto(sendList_json.encode(
                    'utf-8'), (self.dstIP, self.dstPort))
                showText = '\n'.join('hello,' + i for i in recoNames)
                reply = QMessageBox.question(
                    self, 'Info', showText, QMessageBox.Yes)
        elif source.text() == u'暂停':
            self.stopBtn.setText('开始')
            self.stopFlag.emit(1)
        elif source.text() == u'开始':
            self.stopBtn.setText('暂停')
            self.stopFlag.emit(0)
        elif source.text() == u'拍照':
            # if self.stopBtn.text() == '暂停':
            #     self.stopBtn.setText('开始')
            #     self.stopFlag.emit(1)
            self.sp = PhotoShowGui(self.currentFrame)
            # if self.stopBtn.text() == '开始':
            #     self.stopBtn.setText('暂停')
            #     self.stopFlag.emit(0)

    def handleDisplay(self, frame):
        if len(frame):
            self.count += 1
            [b, g, r] = cv2.split(frame)
            frame = cv2.merge([r, g, b])
            self.currentFrame = frame.copy()
            height, width, bytesPerComponent = frame.shape
            self.resize(width + 40, height + 70)
            bytesPerLine = 3 * width
            QImg = QImage(frame.data, width, height,
                          bytesPerLine, QImage.Format_RGB888)
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


class PhotoShowGui(QWidget):
    '''
    用来显示拍照的图片
    '''

    def __init__(self, frame, WinWidth=800, WinHeight=600):
        super(QWidget, self).__init__()
        if frame is None:
            print(u'传入的frame无效')
            self.close()
        self.saveFrame = frame.copy()
        self.WinWidth = frame.shape[1] + 40
        self.WinHeight = frame.shape[0] + 70
        self.initUI()

    def initUI(self):
        '''
        布局设置和控件设置
        :return: QThread

        '''
        self.saveBtn = QPushButton('保存', self)
        self.cancelBtn = QPushButton('取消', self)
        self.saveBtn.clicked.connect(self.clickEvent)
        self.cancelBtn.clicked.connect(self.clickEvent)
        self.scene = QGraphicsScene()
        self.item = QGraphicsPixmapItem()
        height, width, bytesPerComponent = self.saveFrame.shape
        bytesPerLine = 3 * width
        QImg = QImage(self.saveFrame.data, width, height,
                      bytesPerLine, QImage.Format_RGB888)
        self.item.setPixmap(QPixmap.fromImage(QImg))
        self.scene.addItem(self.item)
        self.graphicsview = QGraphicsView()
        self.graphicsview.setScene(self.scene)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.graphicsview)
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.saveBtn)
        hbox.addWidget(self.cancelBtn)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # 窗口设置
        self.resize(self.WinWidth, self.WinHeight)
        self.setWindowTitle("保存图片")
        self.show()

    def clickEvent(self):
        '''
        按下按钮的对话框
        :return: 
        '''
        source = self.sender()
        if source.text() == u'保存':
            filename = QFileDialog.getSaveFileName(self, '保存照片')
            (r, g, b) = cv2.split(self.saveFrame)
            self.saveFrame = cv2.merge([b, g, r])
            cv2.imwrite(filename[0] + '.jpg', self.saveFrame)
            self.close()
        else:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MyWindow()
    app.exec_()
