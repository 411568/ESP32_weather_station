import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # window title
        self.setWindowTitle('Weather station')

        # set starting size
        self.setGeometry(100, 100, 1400, 800)

        # set the layout (grid)
        layout = QGridLayout()
        self.setLayout(layout)

        ############################################ FIGURES ############################################

        #temperature figure
        self.figureTemp = plt.figure(figsize=(5, 5))
        self.figureTempCanvas = FigureCanvas(self.figureTemp)
        layout.addWidget(self.figureTempCanvas, 1, 0)
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
        layout.addWidget(self.figurePressCanvas, 1, 1)
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
        layout.addWidget(self.figureAltCanvas, 1, 2)
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
        layout.addWidget(self.figureHumCanvas, 2, 0)
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
        layout.addWidget(self.figureWindCanvas, 2, 1)
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
        layout.addWidget(self.figureRainCanvas, 2, 2)
        # create an axis
        x = range(0, 10)
        y = range(0, 20, 2)
        bx = self.figureRain.add_subplot(111)
        bx.plot(x, y)
        bx.set_title("Rain sensor")
        # show canvas
        self.figureRainCanvas.show()


        ############################################ Bottom row ############################################

        # for testing only
        battery_level = 0

        # battery level indicator
        battery_level_label = QLabel("Battery status: " + str(battery_level) + "%")
        battery_level_label.setFont(QFont('Times', 20))
        layout.addWidget(battery_level_label, 3, 1, alignment=Qt.AlignCenter)

        # update button
        update_button = QPushButton("Update")
        update_button.setGeometry(0, 0, 200, 10)
        update_button.setFont(QFont('Times', 20))
        update_button.resize(400, 20)
        layout.addWidget(update_button, 3, 0)

        # prediction on/off
        forecast_button = QPushButton("Forecast ON/OFF")
        forecast_button.setFont(QFont('Times', 20))
        update_button.resize(400, 20)
        layout.addWidget(forecast_button, 3, 2)



        # show the window
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
