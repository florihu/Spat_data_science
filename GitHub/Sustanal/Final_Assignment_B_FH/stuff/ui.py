import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtGui
from . water_imput import iteration


class ThresholdSelector(QWidget):

    sliderValueChanged = pyqtSignal(int, int)  # Define the signal here
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Threshold Selector')
        self.setGeometry(1000, 1000, 1000, 500)

        layout = QVBoxLayout()
        # image (shown usually via a QLabel)

        self.label = QLabel(self)
        self.pixmap = QtGui.QPixmap('stuff\porportion_classes_UI.jpeg')
        # Scale the image to the desired width and height
        scaled_pixmap = self.pixmap.scaled(640, 480, aspectRatioMode=Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.update()


        self.slider1 = QSlider()
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(100)
        self.slider1.setOrientation(1)  # Horizontal slider
        self.slider1.valueChanged.connect(self.updateThreshold)

        self.slider2 = QSlider()
        self.slider2.setMinimum(0)
        self.slider2.setMaximum(100)
        self.slider2.setOrientation(1)  # Horizontal slider
        self.slider2.valueChanged.connect(self.updateThreshold)

        self.label1 = QLabel("Threshold 1: 0")
        self.label2 = QLabel("Threshold 2: 0")

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.close)

        layout.addWidget(self.slider1)
        layout.addWidget(self.label1)
        layout.addWidget(self.slider2)
        layout.addWidget(self.label2)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.prev_value1 = 0
        self.prev_value2 = 0



    def updateThreshold(self):
        value1 = self.slider1.value()
        value2 = self.slider2.value()

        if value1 > value2:
            QMessageBox.warning(self, "Warning", "Threshold 1 must be less than or equal to Threshold 2")
            self.slider1.setValue(self.prev_value1)
        else:
            self.prev_value1 = value1
            self.prev_value2 = value2
            self.label1.setText(f"Threshold 1: {value1}")
            self.label2.setText(f"Threshold 2: {value2}")
            self.sliderValueChanged.emit(value1, value2)
            iteration.clustering(self.prev_value1, self.prev_value2)


def start_app():

    app = QApplication(sys.argv)
    window = ThresholdSelector()
    window.show()
    sys.exit(app.exec_())
