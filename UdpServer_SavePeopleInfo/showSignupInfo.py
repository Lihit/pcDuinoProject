#-*- coding:utf-8 -*-
'''
author:wenshao
time:2017-11-3
'''
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import os
from multiprocessing import Process, Queue
import random


class MyThread(QThread):
    updateData = pyqtSignal(list)

    def run(self):
        filePath = 'myfile.txt'
        modifyTime = -1
        try:
            while True:
                fileData = []
                if not os.path.exists(filePath):
                    print('文件不存在')
                    break
                #mtime = time.ctime(os.path.getmtime(filePath))
                if os.access(filePath, os.R_OK):
                    with open(filePath, 'r') as f:
                        for line in f:
                            fileData.append(line.split(','))
                    # print(fileData)
                    #modifyTime = mtime
                else:
                    print('the file does not be read')
                if fileData != []:
                    self.updateData.emit(fileData)
        except Exception as e:
            print('函数MyThread::run出现异常')
            print(e)


class TableSheet(QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()
        for i in range(3):
            #contentList = ['Tag%d' % i, 'CheckIn', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
            contentList = ['', '', '']
            rowCOunt = self.table.rowCount()
            self.insertNewRow(contentList, rowCOunt)

    def initUi(self):
        self.resize(1000, 510)
        horizontalHeader = ["TagName", "Status", "TimeStamp"]
        self.setWindowTitle('MyTable')
        self.table = QTableWidget()
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setColumnCount(3)
        # self.table.setRowCount(3)
        self.table.setHorizontalHeaderLabels(horizontalHeader)
        # self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectColumns)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for index in range(self.table.columnCount()):
            headItem = self.table.horizontalHeaderItem(index)
            headItem.setFont(QFont("song", 16, QFont.Bold))
            headItem.setForeground(QBrush(Qt.gray))
            #headItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)

    def insertNewRow(self, contentList, insertRow):
        if len(contentList) != 3:
            contentList = ['', '', '']
        self.table.insertRow(insertRow)
        self.table.setRowHeight(insertRow, 150)
        for index in range(len(contentList)):
            newItem = QTableWidgetItem(str(contentList[index]))
            newItem.setFont(QFont("Roman times", 40, QFont.Bold))
            newItem.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(insertRow, index, newItem)

    def changeRowContent(self, NewContentList, insertRow):
        if len(NewContentList) != 3:
            NewContentList = ['', '', '']
        if insertRow >= self.table.rowCount():
            insertRow = self.table.rowCount()
            self.table.insertRow(insertRow)
            self.table.setRowHeight(insertRow, 150)
        for index in range(len(NewContentList)):
            newItem = QTableWidgetItem(str(NewContentList[index]).replace('\n',''))
            newItem.setFont(QFont("Roman times", 40, QFont.Bold))
            newItem.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(insertRow, index, newItem)

    def handleDisplay(self, data):
        if len(data):
            for i in range(len(data)):
                if float(data[i][1].strip()) > 0:
                    data[i][1] = 'CheckIn'
                else:
                    data[i][1] = 'CheckOut'
                self.changeRowContent(data[i], i)


def ShowGUI():
    try:
        app = QApplication(sys.argv)
        table = TableSheet()
        myth = MyThread()
        myth.updateData.connect(table.handleDisplay)
        myth.start()
        table.show()
        sys.exit(app.exec_())
    except Exception as e:
        print('函数ShowGUI出现异常')
        print(e)


def writeFile():
    count = 0
    while True:
        if os.access('myfile.txt', os.W_OK):
            with open('myfile.txt', 'w') as fp:
                for i in range(3):
                    fp.write('Tag%i' % random.randint(0, 100) + ',' + str(random.random() - 0.5) +
                             ',' + str(time.strftime("%H:%M:%S", time.localtime())) + '\n')
        print(count)
        count += 1
        if count > 20:
            break
        time.sleep(1)


def main():
    ShowGUI_process = Process(target=ShowGUI)
    writeFile_process = Process(target=writeFile)
    ShowGUI_process.start()
    writeFile_process.start()
    ShowGUI_process.join()
    writeFile_process.join()

if __name__ == '__main__':
    main()
