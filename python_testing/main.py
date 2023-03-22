import sys
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Weather station')

        # set the grid layout
        layout = QGridLayout()
        self.setLayout(layout)

        #temperature figure
        self.figureTemp = plt.figure(figsize=(5, 5))
        self.figureTempCanvas = FigureCanvas(self.figureTemp)
        layout.addWidget(self.figureTempCanvas, 0, 0)
        # create an axis
        x = range(0, 10)
        y = range(0, 20, 2)
        ax = self.figureTemp.add_subplot(111)
        ax.plot(x, y)
        ax.set_title("Temperature")
        # show canvas
        self.figureTempCanvas.show()

        #pressure figure
        self.figurePress = plt.figure(figsize=(5, 5))
        self.figurePressCanvas = FigureCanvas(self.figurePress)
        layout.addWidget(self.figurePressCanvas, 0, 1)
           # create an axis
        x = range(0, 10)
        y = range(0, 50, 5)
        bx = self.figurePress.add_subplot(111)
        bx.plot(x, y)
        bx.set_title("Pressure")
        # show canvas
        self.figurePressCanvas.show()

        # altitude figure
        self.figureAlt = plt.figure(figsize=(5, 5))
        self.figureAltCanvas = FigureCanvas(self.figureAlt)
        layout.addWidget(self.figureAltCanvas, 0, 2)
        # create an axis
        x = range(0, 10)
        y = range(0, 50, 5)
        bx = self.figureAlt.add_subplot(111)
        bx.plot(x, y)
        bx.set_title("Altitude")
        # show canvas
        self.figureAltCanvas.show()

        # humidity figure
        self.figureHum = plt.figure(figsize=(5, 5))
        self.figureHumCanvas = FigureCanvas(self.figureHum)
        layout.addWidget(self.figureHumCanvas, 1, 0)
        # create an axis
        x = range(0, 10)
        y = range(0, 20, 2)
        bx = self.figureHum.add_subplot(111)
        bx.plot(x, y)
        bx.set_title("Humidity")
        # show canvas
        self.figureHumCanvas.show()

        # windspeed figure
        self.figureWind = plt.figure(figsize=(5, 5))
        self.figureWindCanvas = FigureCanvas(self.figureWind)
        layout.addWidget(self.figureWindCanvas, 1, 1)
        # create an axis
        x = range(0, 10)
        y = range(0, 20, 2)
        bx = self.figureWind.add_subplot(111)
        bx.plot(x, y)
        bx.set_title("Wind speed")
        # show canvas
        self.figureWindCanvas.show()

        # rain figure
        self.figureRain = plt.figure(figsize=(5, 5))
        self.figureRainCanvas = FigureCanvas(self.figureRain)
        layout.addWidget(self.figureRainCanvas, 1, 2)
        # create an axis
        x = range(0, 10)
        y = range(0, 20, 2)
        bx = self.figureRain.add_subplot(111)
        bx.plot(x, y)
        bx.set_title("Rain sensor")
        # show canvas
        self.figureRainCanvas.show()

        # username

        # buttons
        layout.addWidget(QPushButton('Update'), 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QPushButton('Prediction ON/OFF'), 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        # show the window
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
