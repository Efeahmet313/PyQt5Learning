import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import requests

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.downloadwidget = Widget(self)
        self.setCentralWidget(self.downloadwidget)

        self.progressBar = QProgressBar(self, minimumWidth=400)
        self.progressBar.setValue(0)
        self.progressBar.move(150, 180)

        self.statusBar()
        openFile = QAction(QIcon('download.png'), 'Download', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Download a File')
        openFile.triggered.connect(self.downloadwidget.showurlDialog)

        self.cancelbtn = QPushButton('cancel', self)
        self.cancelbtn.clicked.connect(QCoreApplication.instance().quit)
        self.cancelbtn.resize(self.cancelbtn.sizeHint())
        self.cancelbtn.move(100, 220)


        self.confirmbtn = QPushButton('confirm', self)
        self.confirmbtn.move(550, 220)
        self.confirmbtn.clicked.connect(self.on_pushButton_clicked)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 750, 300)
        self.setWindowTitle('File dialog')
        self.show()

# 下载部分参考博文 https://blog.csdn.net/qq_20265805/article/details/88899066

#    下载按钮事件
    def on_pushButton_clicked(self):
        the_url = self.downloadwidget.urledit.text()
        the_filesize = requests.get(the_url, stream=True).headers['Content-Length']
        the_filepath = self.downloadwidget.directoryedit.text()
        the_fileobj = open(the_filepath, 'wb')
        #### 创建下载线程
        self.downloadThread = downloadThread(the_url, the_filesize, the_fileobj, buffer=10240)
        self.downloadThread.download_proess_signal.connect(self.set_progressbar_value)
        self.downloadThread.start()

    # 设置进度条
    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            QMessageBox.information(self, "提示", "下载成功！")
            return

class Widget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initwidget()

    def initwidget(self):
        self.urlbtn = QPushButton('url', self)
        self.urlbtn.move(50, 50)
        self.urlbtn.clicked.connect(self.showurlDialog)

        self.urledit = QLineEdit(self)
        self.urledit.move(220, 50)

        self.directorybtn = QPushButton('directory', self)
        self.directorybtn.move(50, 100)
        self.directorybtn.clicked.connect(self.showdirDialog)

        self.directoryedit = QLineEdit(self)
        self.directoryedit.move(220, 100)

    def showurlDialog(self):
        text, ok = QInputDialog.getText(self, 'Input url',
            'Enter url:')
        if ok:
            self.urledit.setText(str(text))
    def showdirDialog(self):
        text, ok = QInputDialog.getText(self, 'Input directory',
            'Enter your directory:')
        if ok:
            self.directoryedit.setText(str(text))
#下载线程
class downloadThread(QThread):
    download_proess_signal = pyqtSignal(int)                        #创建信号

    def __init__(self, url, filesize, fileobj, buffer):
        super(downloadThread, self).__init__()
        self.url = url
        self.filesize = filesize
        self.fileobj = fileobj
        self.buffer = buffer


    def run(self):
        try:
            rsp = requests.get(self.url, stream=True)                #流下载模式
            offset = 0
            for chunk in rsp.iter_content(chunk_size=self.buffer):
                if not chunk: break
                self.fileobj.seek(offset)                            #设置指针位置
                self.fileobj.write(chunk)                            #写入文件
                offset = offset + len(chunk)
                proess = offset / int(self.filesize) * 100
                self.download_proess_signal.emit(int(proess))        #发送信号
            self.fileobj.close()    #关闭文件
            self.exit(0)            #关闭线程


        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
