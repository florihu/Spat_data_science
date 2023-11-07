import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QPushButton, QMessageBox, QDesktopWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtGui
from . water_imput import iteration
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
color_palette = sns.color_palette("husl")
class ThresholdSelector(QWidget):

    sliderValueChanged = pyqtSignal(int, int)  # Define the signal here


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Threshold Selector')
        self.setGeometry(1000, 1000, 1000, 1000)

        layout = QVBoxLayout()
        # image (shown usually via a QLabel)

        #
        # self.label = QLabel(self)
        # self.pixmap = QtGui.QPixmap('Graphs\porportion_classes_UI.jpeg')
        # #Scale the image to the desired width and height
        # scaled_pixmap = self.pixmap.scaled(640, 480, aspectRatioMode=Qt.KeepAspectRatio)
        # self.label.setPixmap(scaled_pixmap)
        # self.label.setAlignment(Qt.AlignCenter)
        #self.label.update()
        self.data = iteration.clustering(25, 50).iloc[:,[0,2,3,4]]

        self.canvas = FigureCanvas(plt.Figure(figsize=(30, 10)))
        layout.addWidget(self.canvas)
        self.insert_ax()


        self.slider1 = QSlider()
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(100)
        self.slider1.setOrientation(1)  # Horizontal slider
        self.slider1.valueChanged.connect(self.updateThreshold)
        self.slider1.valueChanged.connect(self.update_chart)

        self.slider2 = QSlider()
        self.slider2.setMinimum(0)
        self.slider2.setMaximum(100)
        self.slider2.setOrientation(1)  # Horizontal slider
        self.slider2.valueChanged.connect(self.updateThreshold)
        self.slider2.valueChanged.connect(self.update_chart)

        self.label1 = QLabel("Threshold 1: 0")
        self.label2 = QLabel("Threshold 2: 0")

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.close)


        layout.addWidget(self.slider1)
        layout.addWidget(self.label1)
        layout.addWidget(self.slider2)
        layout.addWidget(self.label2)
        layout.addWidget(self.ok_button)
        #layout.addWidget(self.label)

        self.setLayout(layout)

        self.prev_value1 = 0
        self.prev_value2 = 0
        self.ax = self.insert_ax()



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
            self.data = iteration.clustering(self.prev_value1, self.prev_value2).iloc[:,[0,2,3,4]]
            # Update the displayed image without changing the image filename

    def insert_ax(self):
        result_df_percentage = self.data.div(self.data.sum(axis=0), axis=1) * 100
        ax = result_df_percentage.T.plot(kind='barh', stacked=True, color=color_palette, ax=self.canvas.figure.add_subplot(111))
        return ax

    def update_chart(self):
        result_df_percentage = self.data.div(self.data.sum(axis=0), axis=1) * 100
        self.ax.clear()  # Clear the existing plot
        result_df_percentage.T.plot(kind='barh', stacked=True, ax=self.ax, color=color_palette)
        self.canvas.draw()  # Redraw the canvas



def start_app():

    app = QApplication(sys.argv)
    window = ThresholdSelector()
    # Center the window on the screen
    screen = QDesktopWidget().screenGeometry()
    window_size = window.geometry()
    window.move((screen.width() - window_size.width()) // 2, (screen.height() - window_size.height()) // 2)

    # Raise the window to the front
    window.show()
    window.raise_()

    sys.exit(app.exec_())

