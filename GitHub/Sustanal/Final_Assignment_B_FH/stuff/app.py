from PyQt5 import QtWidgets
from . central_widget import CentralWidget


class MyMainWindow(QtWidgets.QMainWindow):

    """
    Our main window.
    """

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setWindowTitle("Roulette Game")
        self.central_w = CentralWidget()
        self.setCentralWidget(self.central_w)  # place the central widget within mainwindow


def start_app():
    qapp = QtWidgets.QApplication([])  # create application
    mainwindow = MyMainWindow()
    mainwindow.show()
    qapp.exec_()  # exec_() monitors application for events (event loop)

