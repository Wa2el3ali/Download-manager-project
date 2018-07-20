from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import os
from os import path
import sys
import urllib.request
import pafy
import humanize

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI()
        self.Handle_Buttons()

    def Handle_UI(self):
        self.setWindowTitle('Python Download Manger')
        self.setFixedSize(529, 270)

    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handle_Browse)
        self.pushButton_3.clicked.connect(self.Save_Browse)
        self.pushButton_6.clicked.connect(self.Handle_Browse)
        self.pushButton_4.clicked.connect(self.Download_Youtube_video)
        self.pushButton_7.clicked.connect(self.Get_Youtube_video)

    def Handle_Browse(self):
        save_place = QFileDialog.getSaveFileName(self, caption='Save as', directory='.', filter='All Files (*.*)')
        self.lineEdit_2.setText(save_place[0])



    def Save_Browse(self):
        save = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_4.setText(save)

    def Handle_Progress(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize

        if totalsize > 0:
            percentage = read * 100 / totalsize
            self.progressBar.setValue(percentage)
            QApplication.processEvents()


    def Get_Youtube_video(self):
        video_link = self.lineEdit_3.text()
        v = pafy.new(video_link)
        # print(v.title)
        # print(v.duration)
        # print(v.rating)
        # print(v.author)
        # print(v.length)
        # print(v.keywords)
        # print(v.thumb)
        # print(v.videoid)
        # print(v.viewcount)
        st = v.allstreams
        print(st)
        for i in st:
            size = humanize.naturalsize(i.get_filesize())
            data = '{} {} {} {}'.format(i.mediatype, i.extension, i.quality, size)
            self.comboBox.addItem(data)

    def Download_Youtube_video(self):
        video_link = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()
        v = pafy.new(video_link)
        st = v.allstreams
        quality = self.comboBox.currentIndex()

        try:
            down = st[quality].download(filepath=save_location)
        except Exception:
            QMessageBox.warning(self, 'Download ERROR', 'The Download Failed')
            return

        QMessageBox.information(self, 'Download Completed', 'The Video Download is Finished')


    def Download(self):
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()


        try:
            urllib.request.urlretrieve(url, save_location, self.Handle_Progress)
        except Exception:
            QMessageBox.warning(self, 'Download ERROR', 'The Download Failed')
            return

        QMessageBox.information(self, 'Download Completed', 'The Download is Finished')
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
