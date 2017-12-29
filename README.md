## 项目简介
可以从摄像头中读取视频并显示出来，在显示出来的视频中可以录入人脸，拍照和进行人脸识别，然后将识别出来的人脸＋姓名＋识别时间发送服务器保存，并可以在服务器端显示出来，从而实现一个人脸打卡系统。

## 编程环境
* 系统：Ubuntu16.04
* 编程语言：python
* python需要安装的库：
    * opencv3
    * sklearn
    * PyQt5
    * face_recognition<br>
在这里只列出了一些必须库，当然还有一些其他常用的python库需要安装，如果运行出错，请自行用`pip install`安装。<br>
而列出来的上述的库是比较难安装的，如果安装出错就联系我吧，下面重点介绍`face_recognition`这个库。
`face_recognition`库是一个可以用来做人脸检测和识别的python开源库，可以通过python或者命令行即可实现人脸识别的功能,使用dlib深度学习人脸识别技术构建，在户外脸部检测数据库基准（Labeled Faces in the Wild）上的准确率为99.38%。 
`https://github.com/ageitgey/face_recognition`这是它在github上的开源地址。下面仅介绍face_recognition的安装步骤，因为安装很容易出错！<br>
    **face_recognition安装步骤**
        * 安装依赖项
            * `sudo apt-get install build-essential cmake`
            * `sudo apt-get install libgtk-3-dev`
            * `sudo apt-get install libboost-all-dev`
        * 安装`dlib`
            * `sudo pip install dlib`
        * 安装`face_recognition`
            * `sudo pip install face_recognition`
## 使用方式
* 先将项目克隆到本地：`git clone https://github.com/Lihit/pcDuinoProject`.
* 到这个项目的根目录下:`cd pcDuinoProject`.
* 可以发现有两个文件夹`FaceRecWithGui`和`UdpServer_SavePeopleInfo`。
* 先进入`UdpServer_SavePeopleInfo`文件夹中，打开终端，运行`pyhton recvInfoAndSave.py`,即可将保存数据到`myfile.txt`文件，如果你想将结果显示出来，再运行`python showSignupInfo.py`。
* 再进入打开终端，运行`python main.py`即可，这里默认设置是打开摄像头进行检测识别，你也可以对视频进行检测和识别，只需要将`main.py`文件里第31行`cap = skvideo.io.VideoCapture(0)`的参数0改成你的视频文件的路径即可。具体的操作可根据Gui界面上的按钮来尝试。
## 项目架构
* pcDuinoProject/:项目名称
    * FaceRecWithGui/:客户端项目
        * FaceRecognition/:人脸检测和识别的模块
            * KnownFaces/:用来保存录入的人脸
            * images_test/:测试用
            * FaceRecognition.py:实现人脸识别和检测的核心文件
            * test.py:测试用
        * FaceShowGui/：
            * FaceShowGui.py:主界面显示程序
        * main.py:客户端的主程序入口
    * UdpServer_SavePeopleInfo/:服务端项目
        * recvInfoAndSave.py:接收客户端发送过来的服务信息并保存
        * showSignupInfo.py:将保存下来的信息显示出来的gui界面
## 结果
* 录入人脸<br>
![Selection_045.png-220kB][1]
* 拍照<br>
![Selection_044.png-279.4kB][2]
* 人脸识别<br>
![Selection_046.png-323.6kB][3]



        


  [1]: http://static.zybuluo.com/wenshao/qqd8njdnuoqrjpg95fk5tvyk/Selection_045.png
  [2]: http://static.zybuluo.com/wenshao/jyu6npji5j1bgq5x9zrq2v14/Selection_044.png
  [3]: http://static.zybuluo.com/wenshao/al2mg66ykz2z4176gbt8a9hy/Selection_046.png
