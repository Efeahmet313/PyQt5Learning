#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we create a more
complicated window layout using
the QGridLayout manager.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QTextEdit, QLabel, QHBoxLayout,
    QLineEdit, QAction, QGridLayout, QPushButton, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys
import hashlib

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.filewidget = filelabel(self)
        self.setCentralWidget(self.filewidget)
        self.statusBar()
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.filewidget.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 750, 300)
        self.setWindowTitle('File dialog')
        self.show()

class filelabel(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.initfilelabel()

    def initfilelabel(self):
        self.FileName = QLabel('FileName')
        self.FileMd5 = QLabel('FileMd5')

        self.FileNameEdit = QLineEdit()
        self.FileMd5Edit = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.FileName, 1, 0)
        grid.addWidget(self.FileNameEdit, 1, 1)

        grid.addWidget(self.FileMd5, 2, 0)
        grid.addWidget(self.FileMd5Edit, 2, 1)

        self.setLayout(grid)
    def showDialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/User/xuyetao/Document')
        if fname[0]:
            f = open(fname[0], 'rb')
            md5_obj = hashlib.md5()
            md5_obj.update(f.read())
            hash_code = md5_obj.hexdigest()
            f.close()
            md5 = str(hash_code).lower()
            self.FileNameEdit.setText(fname[0])
            self.FileMd5Edit.setText(md5)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

